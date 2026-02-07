# 快速开始指南

## 一、准备Linux环境（Windows用户）

### 安装WSL2

```powershell
# 在PowerShell（管理员）中运行
wsl --install -d Ubuntu-20.04

# 重启电脑

# 启动Ubuntu
wsl

# 更新系统
sudo apt update && sudo apt upgrade -y
```

## 二、一键安装脚本

### 自动安装所有依赖

```bash
cd StockAnalysisAndroid

# 赋予执行权限
chmod +x setup.sh

# 运行安装脚本
./setup.sh
```

如果没有`setup.sh`，手动执行以下命令：

```bash
# 1. 安装系统依赖
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip python3-dev \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev build-essential ccache

# 2. 安装Buildozer
pip3 install buildozer cython==0.29.36

# 3. 验证
buildozer --version
```

## 三、构建APK

### 方式1: 快速构建（推荐新手）

```bash
# 一键构建调试版
buildozer -v android debug

# 等待1-2小时（首次）
# APK路径: bin/stockanalysis-1.0.0-debug.apk
```

### 方式2: 分步构建（推荐开发者）

```bash
# 步骤1: 初始化
buildozer init

# 步骤2: 下载依赖（可能需要30分钟）
buildozer android update

# 步骤3: 构建（可能需要1小时）
buildozer -v android debug
```

## 四、安装到手机

### USB连接方式

```bash
# 1. 手机开启开发者模式和USB调试

# 2. 连接手机到电脑

# 3. 验证连接
adb devices

# 4. 安装APK
adb install bin/stockanalysis-1.0.0-debug.apk
```

### 文件传输方式

```bash
# 1. 将APK发送到手机（通过微信、QQ等）

# 2. 在手机上打开APK文件

# 3. 允许安装未知来源应用

# 4. 点击安装
```

## 五、首次使用

### 1. 启动应用

点击应用图标 "股票分析"

### 2. 授予权限

应用会请求以下权限，请全部**允许**：

- [ ] 存储权限
- [ ] 网络权限
- [ ] 后台运行权限

### 3. 下载数据

1. 点击"下载数据"按钮
2. 等待30-40分钟（首次）
3. 观察状态栏进度

### 4. 查看结果

下载完成后，自动显示分析结果。

### 5. 设置定时任务

1. 进入手机系统设置
2. 找到"股票分析"应用
3. 关闭"电池优化"
4. 允许"后台运行"

## 六、日常使用

### 自动模式（推荐）

应用会在每天**15:30**自动更新数据，无需手动操作。

### 手动模式

随时点击"下载数据"按钮进行更新。

## 七、故障排除

### 应用无法启动

```bash
# 卸载重装
adb uninstall com.tradeanalytics.stockanalysis

# 清理数据
adb shell rm -rf /storage/emulated/0/StockAnalysis/

# 重新安装
adb install bin/stockanalysis-1.0.0-debug.apk
```

### 下载失败

1. 检查网络连接
2. 切换WiFi网络
3. 重启应用重试

### 定时任务不工作

1. 检查后台运行权限
2. 关闭电池优化
3. 重启应用

## 八、开发者选项

### 本地测试

在构建APK前，可以先在桌面测试：

```bash
# 安装依赖
pip install kivy pandas numpy matplotlib

# 运行
python main.py
```

### 查看日志

```bash
# 通过ADB查看实时日志
adb logcat | grep python

# 或导出日志
adb pull /storage/emulated/0/StockAnalysis/logs/ ./logs_backup/
```

### 修改代码后重新构建

```bash
# 快速增量构建
buildozer -v android debug

# 完全重新构建
buildozer android clean
buildozer -v android debug
```

## 九、更新应用

### 版本更新

1. 修改`main.py`中的`__version__`
2. 修改`buildozer.spec`中的`version`
3. 重新构建APK
4. 覆盖安装（保留数据）

```bash
adb install -r bin/stockanalysis-1.0.0-debug.apk
```

## 十、联系支持

- GitHub Issues: [项目链接]
- Email: [联系邮箱]
- 文档: README.md, BUILD_GUIDE.md

---

**祝您使用愉快！**
