# 股票分析安卓应用

基于Python + Kivy开发的安卓股票分析应用，功能与桌面版TradeAnalytics完全对等。

## 功能特性

- 自动下载沪深A股所有股票数据
- 计算120日移动平均线
- 成交量暴涨分析（前7天平均量的5倍以上）
- 股票筛选和结果展示
- 量价图表可视化
- 后台定时任务（每日15:30自动执行）
- 本地数据存储

## 技术栈

- **前端**: Kivy (Python UI框架)
- **业务逻辑**: 复用TradeAnalytics核心代码（90%+）
- **数据源**: BaoStock
- **数据处理**: pandas, numpy
- **图表**: matplotlib
- **打包**: Buildozer

## 开发环境

### 系统要求

- Ubuntu 20.04+ / Debian 11+
- Python 3.9+
- 至少8GB RAM
- 至少30GB可用磁盘空间

### 安装依赖

```bash
# 安装系统依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装Python依赖
pip3 install -r requirements.txt
```

## 构建APK

### 首次构建

```bash
# 初始化buildozer
buildozer init

# 构建调试版APK
buildozer -v android debug

# APK位置：bin/stockanalysis-1.0.0-debug.apk
```

### 清理构建

```bash
buildozer android clean
```

### 发布版本

```bash
buildozer -v android release
```

## 安装测试

```bash
# 通过ADB安装
adb install bin/stockanalysis-1.0.0-debug.apk

# 查看日志
adb logcat | grep python
```

## 项目结构

```
StockAnalysisAndroid/
├── main.py                 # 应用入口
├── service.py             # 后台服务
├── buildozer.spec         # 打包配置
├── requirements.txt       # Python依赖
├── src/
│   ├── ui/               # Kivy UI层
│   ├── core/             # 业务逻辑（复用）
│   ├── storage/          # 数据存储
│   └── scheduler/        # 后台任务
└── assets/              # 资源文件
```

## 代码复用

从TradeAnalytics复用以下模块（90%+）：

- ✓ data_downloader.py（轻微改造）
- ✓ data_analyzer.py（完全复用）
- ✓ stock_filter.py（完全复用）
- ✓ volume_analyzer.py（完全复用）
- ✓ data_source_baostock_threadsafe.py（完全复用）
- ✓ utils.py（调整路径）

## 注意事项

1. 首次构建需要下载Android SDK/NDK，需要1-2小时
2. APK大小约50-80MB（包含Python运行时）
3. 建议在物理设备上测试，模拟器性能较差
4. 后台服务需要用户关闭电池优化

## 许可证

与TradeAnalytics相同，仅供学习研究使用。
