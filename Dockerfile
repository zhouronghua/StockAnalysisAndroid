FROM ubuntu:20.04

LABEL maintainer="StockAnalysis"
LABEL description="Docker环境用于构建Android APK"

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
ENV PATH="${PATH}:${ANDROID_HOME}/tools:${ANDROID_HOME}/platform-tools"
ENV LANG=C.UTF-8

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-11-jdk \
    wget \
    python3 \
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
    ccache \
    && rm -rf /var/lib/apt/lists/*

# 升级pip
RUN pip3 install --upgrade pip setuptools wheel

# 安装Buildozer和Cython
RUN pip3 install buildozer cython==0.29.36

# 设置工作目录
WORKDIR /app

# 复制项目文件（使用.dockerignore排除不必要的文件）
COPY . /app

# 创建必要的目录
RUN mkdir -p /root/.buildozer

# 默认命令
CMD ["buildozer", "-v", "android", "debug"]
