# 使用Docker在Windows上构建APK

## 前提条件

- Windows 10 Pro/Enterprise/Education 或 Windows 11
- 至少8GB内存
- 至少20GB可用磁盘空间

## 安装Docker Desktop

### 1. 下载Docker Desktop

访问: https://www.docker.com/products/docker-desktop/

点击"Download for Windows"

### 2. 安装

双击安装程序，按照提示安装。

**注意**: 
- 会提示安装WSL2，允许安装
- 安装完成后需要重启电脑

### 3. 启动Docker Desktop

- 从开始菜单启动"Docker Desktop"
- 等待Docker引擎启动（状态栏显示绿色）

### 4. 验证安装

打开PowerShell，运行：

```powershell
docker --version
# 应该显示: Docker version 24.x.x

docker run hello-world
# 应该显示: Hello from Docker!
```

## 使用Docker构建APK

### 方式1: 使用Dockerfile（推荐）

#### 1. 进入项目目录

```powershell
cd E:\code\TradeAnalytics\StockAnalysisAndroid
```

#### 2. 构建Docker镜像（首次，约10-15分钟）

```powershell
docker build -t stockanalysis-builder .
```

这会：
- 创建Ubuntu环境
- 安装所有依赖
- 准备构建环境

#### 3. 运行构建（首次约1-2小时）

```powershell
docker run --rm -v ${PWD}:/app stockanalysis-builder
```

#### 4. 查看生成的APK

```powershell
ls bin\
# 应该看到: stockanalysis-1.0.0-debug.apk
```

### 方式2: 交互式构建

如果需要调试或查看构建过程：

```powershell
# 进入容器
docker run -it --rm -v ${PWD}:/app stockanalysis-builder bash

# 在容器内手动构建
buildozer -v android debug

# 查看日志
cat .buildozer/logs/buildozer.log

# 退出容器
exit
```

## 后续构建

### 快速重新构建

```powershell
# 修改代码后，直接运行
docker run --rm -v ${PWD}:/app stockanalysis-builder
```

### 清理旧的构建

```powershell
# 删除bin目录
Remove-Item -Recurse -Force bin\

# 清理buildozer缓存（可选）
Remove-Item -Recurse -Force .buildozer\
```

## Docker命令参考

### 查看镜像

```powershell
docker images
```

### 删除镜像

```powershell
docker rmi stockanalysis-builder
```

### 查看运行中的容器

```powershell
docker ps
```

### 停止容器

```powershell
docker stop <容器ID>
```

### 清理所有停止的容器

```powershell
docker container prune
```

## 优化技巧

### 1. 使用缓存加速构建

修改Dockerfile，添加缓存卷：

```dockerfile
# 在Dockerfile末尾添加
VOLUME ["/root/.buildozer"]
```

创建命名卷：

```powershell
docker volume create buildozer-cache

docker run --rm \
  -v ${PWD}:/app \
  -v buildozer-cache:/root/.buildozer \
  stockanalysis-builder
```

第二次构建会快很多（约15-20分钟）。

### 2. 查看构建日志

```powershell
# 实时查看日志
docker run --rm -v ${PWD}:/app stockanalysis-builder 2>&1 | Tee-Object -FilePath build.log
```

### 3. 限制资源使用

```powershell
# 限制内存和CPU
docker run --rm \
  -v ${PWD}:/app \
  --memory=4g \
  --cpus=2 \
  stockanalysis-builder
```

## 常见问题

### 问题1: Docker Desktop无法启动

**原因**: 虚拟化未启用

**解决**:
1. 重启电脑进入BIOS
2. 启用"Intel VT-x"或"AMD-V"
3. 保存并重启

### 问题2: "docker: command not found"

**原因**: Docker Desktop未正确安装或未启动

**解决**:
1. 确保Docker Desktop正在运行
2. 重启Docker Desktop
3. 重新安装Docker Desktop

### 问题3: 构建很慢

**原因**: 首次构建需要下载大量依赖

**解决**:
- 首次构建需要1-2小时，这是正常的
- 使用缓存卷可以大幅加速后续构建
- 确保网络连接良好

### 问题4: "no space left on device"

**原因**: Docker磁盘空间不足

**解决**:
```powershell
# 清理未使用的资源
docker system prune -a

# 或在Docker Desktop设置中增加磁盘空间
# 设置 -> Resources -> Disk image size
```

### 问题5: 无法访问Windows文件

**原因**: 文件共享未启用

**解决**:
1. Docker Desktop -> Settings -> Resources -> File Sharing
2. 添加项目所在驱动器（如E:）
3. Apply & Restart

## 性能对比

| 环境 | 首次构建 | 后续构建 | 内存占用 |
|------|---------|---------|---------|
| Docker（无缓存） | 1-2小时 | 1-2小时 | 4-6GB |
| Docker（有缓存） | 1-2小时 | 15-20分钟 | 4-6GB |
| WSL2 | 1-2小时 | 10-15分钟 | 2-4GB |
| GitHub Actions | 40-60分钟 | 15-20分钟 | 0（云端） |

## 高级配置

### 多阶段构建

创建更小的镜像：

```dockerfile
# 构建阶段
FROM ubuntu:20.04 as builder
# ... 安装依赖和构建 ...

# 运行阶段
FROM ubuntu:20.04
COPY --from=builder /app/bin /app/bin
CMD ["cat", "/app/bin/stockanalysis-1.0.0-debug.apk"]
```

### 使用Docker Compose

创建`docker-compose.yml`:

```yaml
version: '3.8'
services:
  builder:
    build: .
    volumes:
      - .:/app
      - buildozer-cache:/root/.buildozer
    environment:
      - BUILDOZER_WARN_ON_ROOT=0

volumes:
  buildozer-cache:
```

使用：

```powershell
docker-compose up
```

## 总结

### 优点
- ✅ 不需要WSL2（虽然Docker Desktop内部使用WSL2）
- ✅ 环境隔离，不影响Windows系统
- ✅ 可重复使用，适合CI/CD
- ✅ 支持Windows、Mac、Linux

### 缺点
- ⚠️ 需要安装Docker Desktop（约1GB）
- ⚠️ 首次构建较慢
- ⚠️ 占用内存较高（4-6GB）

### 适用场景
- 不想直接安装WSL2
- 需要环境隔离
- 有Docker使用经验
- 本地构建需求频繁

---

**下一步**: 如果觉得Docker太重，建议使用GitHub Actions（完全云端构建）
