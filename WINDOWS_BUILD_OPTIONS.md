# Windows上构建APK的所有方案

## 方案对比

| 方案 | 难度 | 速度 | 占用资源 | 推荐度 |
|------|------|------|---------|--------|
| GitHub Actions | ⭐ 简单 | 中等 | 0（云端） | ⭐⭐⭐⭐⭐ |
| Docker Desktop | ⭐⭐ 中等 | 快 | 高 | ⭐⭐⭐⭐ |
| VirtualBox虚拟机 | ⭐⭐⭐ 复杂 | 快 | 很高 | ⭐⭐⭐ |
| Google Colab | ⭐⭐ 中等 | 快 | 0（云端） | ⭐⭐ |
| WSL2 | ⭐⭐ 中等 | 最快 | 中等 | ⭐⭐⭐⭐ |

---

## 方案1: GitHub Actions（最推荐）

### 优点
- ✅ 完全不需要配置本地环境
- ✅ 免费（每月2000分钟）
- ✅ 不占用本地资源
- ✅ 自动化构建
- ✅ 适合团队协作

### 缺点
- ⚠️ 需要上传代码到GitHub
- ⚠️ 首次构建较慢（40-60分钟）
- ⚠️ 需要网络连接

### 使用方法
详见: `GITHUB_ACTIONS_GUIDE.md`

### 快速开始
```bash
# 1. 创建GitHub仓库并上传代码
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/StockAnalysisAndroid.git
git push -u origin main

# 2. 访问仓库的Actions页面查看构建进度
# 3. 构建完成后下载APK
```

---

## 方案2: Docker Desktop for Windows

### 优点
- ✅ 本地构建，速度快
- ✅ 环境隔离，不影响系统
- ✅ 可重复使用
- ✅ 类似Linux环境

### 缺点
- ⚠️ 需要安装Docker Desktop（约1GB）
- ⚠️ 占用内存较高（4-8GB）
- ⚠️ 需要Hyper-V或WSL2支持

### 安装步骤

#### 1. 安装Docker Desktop

下载地址: https://www.docker.com/products/docker-desktop/

#### 2. 创建Dockerfile

在`StockAnalysisAndroid`目录创建`Dockerfile`:

```dockerfile
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk

# 安装依赖
RUN apt-get update && apt-get install -y \
    git zip unzip openjdk-11-jdk wget \
    python3-pip python3-dev autoconf libtool \
    pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake \
    libffi-dev libssl-dev build-essential ccache \
    && rm -rf /var/lib/apt/lists/*

# 安装Buildozer
RUN pip3 install --upgrade pip && \
    pip3 install buildozer cython==0.29.36

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 构建命令
CMD ["buildozer", "-v", "android", "debug"]
```

#### 3. 构建Docker镜像

```powershell
# 在PowerShell中运行
cd E:\code\TradeAnalytics\StockAnalysisAndroid
docker build -t stockanalysis-builder .
```

#### 4. 运行构建

```powershell
# 构建APK
docker run --rm -v ${PWD}:/app stockanalysis-builder

# APK会生成在 bin/ 目录
```

#### 5. 后续构建

```powershell
# 快速重新构建
docker run --rm -v ${PWD}:/app stockanalysis-builder
```

---

## 方案3: VirtualBox虚拟机

### 优点
- ✅ 完整的Linux环境
- ✅ 性能好
- ✅ 可以保存多个快照

### 缺点
- ⚠️ 安装配置复杂
- ⚠️ 占用磁盘空间大（20GB+）
- ⚠️ 占用内存高（4GB+）

### 安装步骤

#### 1. 下载并安装VirtualBox

下载地址: https://www.virtualbox.org/wiki/Downloads

#### 2. 下载Ubuntu ISO

下载地址: https://ubuntu.com/download/desktop
选择: Ubuntu 20.04 LTS

#### 3. 创建虚拟机

- 内存: 至少4GB
- 硬盘: 至少30GB
- 处理器: 至少2核心

#### 4. 安装Ubuntu

按照向导安装Ubuntu系统。

#### 5. 共享文件夹

在VirtualBox中设置共享文件夹，映射Windows项目目录。

#### 6. 在虚拟机中构建

```bash
# 进入共享文件夹
cd /mnt/shared/StockAnalysisAndroid

# 运行安装脚本
./setup.sh

# 构建APK
buildozer -v android debug
```

---

## 方案4: Google Colab（实验性）

### 优点
- ✅ 完全免费
- ✅ 不占用本地资源
- ✅ GPU加速（可选）

### 缺点
- ⚠️ 会话限制（12小时）
- ⚠️ 配置复杂
- ⚠️ 不适合频繁构建

### 使用步骤

1. 访问: https://colab.research.google.com/
2. 创建新笔记本
3. 执行以下代码:

```python
# 安装依赖
!apt-get update
!apt-get install -y git zip unzip openjdk-11-jdk wget \
    python3-pip autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 cmake \
    libffi-dev libssl-dev build-essential

# 安装Buildozer
!pip install buildozer cython==0.29.36

# 克隆项目
!git clone https://github.com/你的用户名/StockAnalysisAndroid.git
%cd StockAnalysisAndroid

# 构建APK
!buildozer -v android debug

# 下载APK
from google.colab import files
files.download('bin/stockanalysis-1.0.0-debug.apk')
```

---

## 方案5: 在线CI/CD服务

### CircleCI

免费额度: 每月6000分钟

配置文件 `.circleci/config.yml`:

```yaml
version: 2.1
jobs:
  build:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run: sudo apt-get update && sudo apt-get install -y openjdk-11-jdk
      - run: pip install buildozer cython==0.29.36
      - run: buildozer -v android debug
      - store_artifacts:
          path: bin/
```

### GitLab CI/CD

免费额度: 每月400分钟

配置文件 `.gitlab-ci.yml`:

```yaml
build_apk:
  image: ubuntu:20.04
  script:
    - apt-get update && apt-get install -y python3-pip openjdk-11-jdk
    - pip3 install buildozer cython==0.29.36
    - buildozer -v android debug
  artifacts:
    paths:
      - bin/*.apk
```

---

## 推荐方案总结

### 最简单: GitHub Actions ⭐⭐⭐⭐⭐
- 适合: 所有用户
- 推送代码即可自动构建
- 完全免费，不需要本地配置

### 最快速: Docker Desktop ⭐⭐⭐⭐
- 适合: 有Docker使用经验的用户
- 本地构建，速度快
- 需要安装Docker Desktop

### 最灵活: VirtualBox ⭐⭐⭐
- 适合: 需要完整Linux环境的用户
- 配置复杂但功能全面

### 最省事: WSL2 ⭐⭐⭐⭐
- 适合: Windows 10/11用户
- 安装简单（一条命令）
- 性能接近原生Linux

---

## 具体建议

### 如果您...

- **只想快速构建一次APK**: 用GitHub Actions
- **需要频繁构建**: 装WSL2或Docker
- **完全不想装软件**: 用GitHub Actions或Google Colab
- **团队协作**: 用GitHub Actions
- **学习Linux**: 装WSL2或VirtualBox

---

## 最终推荐

**首选**: GitHub Actions（零配置，零占用）  
**备选**: Docker Desktop（本地快速构建）  
**终极**: WSL2（最接近原生Linux体验）

---

**选择GitHub Actions的理由**:
1. 不需要安装任何Linux环境
2. 完全免费
3. 自动化构建
4. 适合Windows用户

详细使用方法请查看 `GITHUB_ACTIONS_GUIDE.md`
