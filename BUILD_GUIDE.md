# 安卓APK构建指南

## 前置条件

### 1. 操作系统

**推荐**: Ubuntu 20.04+ 或 Debian 11+

**Windows用户**: 建议使用WSL2 (Windows Subsystem for Linux)

```bash
# 安装WSL2
wsl --install -d Ubuntu-20.04
```

### 2. 系统依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要的开发工具
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    python3-pip \
    python3-dev \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    libltdl-dev \
    ccache

# 安装32位库（用于Android SDK）
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386
```

### 3. Python环境

```bash
# 安装Python 3.9
sudo apt install python3.9 python3.9-dev python3.9-venv

# 创建虚拟环境（推荐）
python3.9 -m venv venv
source venv/bin/activate

# 升级pip
pip install --upgrade pip setuptools wheel
```

### 4. 安装Buildozer

```bash
# 安装Buildozer和Cython
pip install buildozer cython==0.29.36

# 验证安装
buildozer --version
```

## 构建步骤

### 1. 进入项目目录

```bash
cd StockAnalysisAndroid
```

### 2. 首次构建（约1-2小时）

```bash
# 初始化buildozer
buildozer init

# 构建调试版APK
buildozer -v android debug
```

**说明**:
- 首次构建会自动下载Android SDK (约1GB) 和 NDK (约1GB)
- 编译所有Python依赖包（pandas, numpy, matplotlib等）
- 总下载量约3-4GB，构建时间1-2小时

### 3. 后续构建（约10-20分钟）

```bash
# 清理缓存（可选）
buildozer android clean

# 重新构建
buildozer -v android debug
```

### 4. 查找生成的APK

```bash
ls -lh bin/
# 文件: bin/stockanalysis-1.0.0-debug.apk
```

## 安装测试

### 1. 通过USB连接手机

```bash
# 手机开启USB调试模式
# 设置 -> 关于手机 -> 连续点击版本号7次 -> 返回 -> 开发者选项 -> 开启USB调试

# 安装ADB工具
sudo apt install adb

# 验证连接
adb devices
```

### 2. 安装APK

```bash
# 安装调试版
adb install bin/stockanalysis-1.0.0-debug.apk

# 如果已安装，覆盖安装
adb install -r bin/stockanalysis-1.0.0-debug.apk
```

### 3. 查看日志

```bash
# 实时查看应用日志
adb logcat | grep python

# 或者过滤stock关键词
adb logcat | grep -i stock
```

## 构建发布版本

### 1. 生成签名密钥

```bash
keytool -genkey -v \
    -keystore stockanalysis.keystore \
    -alias stockanalysis \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000

# 妥善保管生成的 stockanalysis.keystore 文件
```

### 2. 配置buildozer.spec

在`buildozer.spec`中添加：

```ini
[app]
android.release_artifact = aab

[buildozer]
android.keystore = stockanalysis.keystore
android.keystore_alias = stockanalysis
```

### 3. 构建发布版

```bash
# 构建AAB（Google Play推荐）
buildozer -v android release

# 或构建APK
buildozer -v android release
```

## 常见问题

### 问题1: Buildozer下载超时

```bash
# 手动下载SDK/NDK，放到 ~/.buildozer/android/ 目录
# 或者使用国内镜像
export ANDROID_SDK_HOME=$HOME/.buildozer/android/platform/android-sdk
```

### 问题2: 编译pandas/numpy失败

```bash
# 安装预编译轮子
pip install --upgrade pip
pip download pandas==1.5.3 --platform android --only-binary :all:

# 或降低版本
# requirements.txt:
# pandas==1.3.5
# numpy==1.22.4
```

### 问题3: APK体积过大

当前APK预计大小: 50-80MB

**优化方法**:
1. 移除不必要的matplotlib后端
2. 使用ProGuard压缩
3. 只打包arm64-v8a架构

```ini
# buildozer.spec
android.arch = arm64-v8a
```

### 问题4: 安装后闪退

```bash
# 查看崩溃日志
adb logcat | grep -E "python|FATAL"

# 检查权限
adb shell pm list permissions -d -g
```

## 性能优化建议

### 1. 减少APK大小

```ini
# buildozer.spec
source.exclude_dirs = tests, doc, .git, __pycache__
source.exclude_patterns = *.pyc, *.pyo, *.spec
```

### 2. 加快构建速度

```bash
# 使用ccache
export USE_CCACHE=1

# 增加并发编译
export MAKEFLAGS=-j8
```

### 3. 清理构建缓存

```bash
rm -rf .buildozer
buildozer android clean
```

## 目标设备要求

- **最低版本**: Android 5.1 (API 21)
- **推荐版本**: Android 8.0+ (API 26+)
- **存储空间**: 至少500MB可用空间
- **内存**: 至少2GB RAM
- **CPU**: ARMv7或ARM64架构

## 调试技巧

### 1. 桌面环境测试

```bash
# 先在桌面环境测试UI
python main.py
```

### 2. 查看构建日志

```bash
# Buildozer会保存详细日志
cat .buildozer/logs/buildozer.log
```

### 3. 增量构建

```bash
# 只重新编译Python代码，不重新下载SDK
buildozer -v android debug
```

## 参考资源

- Buildozer文档: https://buildozer.readthedocs.io/
- Kivy文档: https://kivy.org/doc/stable/
- Python-for-Android: https://python-for-android.readthedocs.io/
