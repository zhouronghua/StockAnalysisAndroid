#!/bin/bash
# 将TradeAnalytics项目的数据传输到Android设备
# 使用方法: ./transfer_data.sh

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}股票分析Android应用 - 数据传输工具${NC}"
echo "========================================"

# 检查adb命令
if ! command -v adb &> /dev/null; then
    echo -e "${RED}错误: 未找到adb命令${NC}"
    echo "请安装Android SDK Platform Tools"
    exit 1
fi

# 检查设备连接
echo -e "${YELLOW}检查设备连接...${NC}"
devices=$(adb devices | grep -v "List" | grep "device$" | wc -l)
if [ $devices -eq 0 ]; then
    echo -e "${RED}错误: 未检测到Android设备${NC}"
    echo "请确保："
    echo "1. 手机已通过USB连接到电脑"
    echo "2. 手机已开启USB调试模式"
    echo "3. 已授权电脑进行调试"
    exit 1
fi

echo -e "${GREEN}✓ 检测到设备${NC}"

# 源数据目录
SOURCE_DIR="../TradeAnalytics/data"

# 检查源数据目录
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}错误: 未找到TradeAnalytics数据目录${NC}"
    echo "请确保TradeAnalytics项目位于: ../TradeAnalytics/"
    exit 1
fi

# 目标应用包名
PACKAGE="com.tradeanalytics.stockanalysis"

# 目标目录
TARGET_DIR="/data/data/${PACKAGE}/files"

echo ""
echo -e "${YELLOW}准备传输数据...${NC}"

# 检查应用是否已安装
if ! adb shell pm list packages | grep -q "$PACKAGE"; then
    echo -e "${RED}错误: 应用未安装${NC}"
    echo "请先安装APK文件"
    exit 1
fi

echo -e "${GREEN}✓ 应用已安装${NC}"

# 创建目标目录
echo -e "${YELLOW}创建目录结构...${NC}"
adb shell "run-as ${PACKAGE} mkdir -p ${TARGET_DIR}/daily" 2>/dev/null || true
adb shell "run-as ${PACKAGE} mkdir -p ${TARGET_DIR}/stocks" 2>/dev/null || true
adb shell "run-as ${PACKAGE} mkdir -p ${TARGET_DIR}/results" 2>/dev/null || true

# 统计文件数量
daily_count=$(find ${SOURCE_DIR}/daily -name "*.csv" 2>/dev/null | wc -l)
stock_list_exists="no"
if [ -f "${SOURCE_DIR}/stocks/stock_list.csv" ]; then
    stock_list_exists="yes"
fi

echo ""
echo "数据统计："
echo "- 股票历史数据: ${daily_count} 个文件"
echo "- 股票列表: ${stock_list_exists}"
echo ""

# 询问是否继续
read -p "是否继续传输？ (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 传输股票列表
if [ "$stock_list_exists" = "yes" ]; then
    echo -e "${YELLOW}传输股票列表...${NC}"
    
    # 由于run-as限制，需要先push到临时目录再移动
    temp_dir="/sdcard/StockAnalysisTemp"
    adb shell "mkdir -p ${temp_dir}/stocks"
    adb push "${SOURCE_DIR}/stocks/stock_list.csv" "${temp_dir}/stocks/"
    adb shell "run-as ${PACKAGE} cp ${temp_dir}/stocks/stock_list.csv ${TARGET_DIR}/stocks/"
    
    echo -e "${GREEN}✓ 股票列表传输完成${NC}"
fi

# 传输历史数据（分批）
if [ $daily_count -gt 0 ]; then
    echo -e "${YELLOW}传输历史数据 (共 ${daily_count} 个文件)...${NC}"
    echo "这可能需要几分钟时间，请耐心等待..."
    
    # 先push到临时目录
    adb shell "mkdir -p ${temp_dir}/daily"
    adb push "${SOURCE_DIR}/daily/" "${temp_dir}/"
    
    # 然后移动到应用私有目录
    echo -e "${YELLOW}移动文件到应用目录...${NC}"
    adb shell "run-as ${PACKAGE} cp -r ${temp_dir}/daily/* ${TARGET_DIR}/daily/"
    
    echo -e "${GREEN}✓ 历史数据传输完成${NC}"
fi

# 清理临时文件
echo -e "${YELLOW}清理临时文件...${NC}"
adb shell "rm -rf ${temp_dir}"

# 验证传输
echo ""
echo -e "${YELLOW}验证传输结果...${NC}"
transferred_count=$(adb shell "run-as ${PACKAGE} ls ${TARGET_DIR}/daily | wc -l" 2>/dev/null | tr -d '\r')
echo "目标目录文件数: ${transferred_count}"

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}数据传输完成！${NC}"
echo ""
echo "现在可以："
echo "1. 打开股票分析应用"
echo "2. 点击'成交量分析'开始分析"
echo "3. 在'历史记录'中查看结果"
echo ""
