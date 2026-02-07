#!/bin/bash

# 安卓应用环境安装脚本

echo "=================================================="
echo "股票分析安卓应用 - 环境安装脚本"
echo "=================================================="

# 检测操作系统
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "错误: 此脚本仅支持Linux系统"
    echo "Windows用户请使用WSL2"
    exit 1
fi

# 更新系统
echo ""
echo "[1/5] 更新系统包..."
sudo apt update

# 安装系统依赖
echo ""
echo "[2/5] 安装系统依赖..."
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
    ccache

# 安装32位库
echo ""
echo "[3/5] 安装32位库（用于Android SDK）..."
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install -y \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386 \
    lib32z1 \
    libbz2-1.0:i386

# 安装Python依赖
echo ""
echo "[4/5] 安装Python依赖..."
pip3 install --upgrade pip setuptools wheel
pip3 install buildozer cython==0.29.36

# 验证安装
echo ""
echo "[5/5] 验证安装..."
echo ""
echo "Python版本:"
python3 --version

echo ""
echo "Buildozer版本:"
buildozer --version

echo ""
echo "=================================================="
echo "安装完成！"
echo "=================================================="
echo ""
echo "下一步: 构建APK"
echo "  运行命令: buildozer -v android debug"
echo ""
echo "首次构建需要下载Android SDK/NDK，约需1-2小时"
echo "=================================================="
