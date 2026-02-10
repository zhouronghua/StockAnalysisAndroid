# 股票分析Android应用使用说明

## 功能概览

### 1. 主界面（HomeScreen）
- 显示应用状态和数据统计
- 快速访问各功能模块
- 显示当前已下载的股票数据量

### 2. 成交量分析（VolumeAnalysisScreen）
**分析规则：**
- 当天成交量 >= 前7天平均成交量的5倍
- 收盘价 > 均线（自动选择120/60/30/10日均线）

**使用方法：**
1. 点击"成交量分析"进入分析界面
2. 点击"开始分析"执行分析
3. 等待分析完成，查看结果
4. 结果显示：股票代码、名称、成交量倍数、日期
5. 分析结果会自动保存到历史记录

**结果说明：**
- 按成交量倍数从高到低排序
- 显示最新一天符合条件的数据
- 倍数越高表示成交量放大越明显

### 3. 历史记录（HistoryScreen）
**功能：**
- 查看所有历史分析结果
- 按时间倒序显示
- 点击"查看"查看详细结果

**使用方法：**
1. 点击"历史记录"进入
2. 浏览历史分析记录列表
3. 点击任一记录的"查看"按钮查看详情
4. 在详情页面点击"返回列表"回到列表

### 4. 设置（SettingsScreen）
- 显示应用版本信息
- 显示数据存储路径
- 功能说明文档

## 数据准备

### 方式1：使用PC端下载数据后传输

1. 在PC端运行TradeAnalytics项目下载数据：
   ```bash
   cd /home/ronghua.zhou/work/code/TradeAnalytics
   python main.py
   ```

2. 将`data/daily/`目录中的CSV文件传输到手机：
   - Android存储路径：`/data/data/com.tradeanalytics.stockanalysis/files/daily/`
   - 可以使用adb命令：
     ```bash
     adb push data/daily/*.csv /data/data/com.tradeanalytics.stockanalysis/files/daily/
     ```

3. 同样传输股票列表文件：
   ```bash
   adb push data/stocks/stock_list.csv /data/data/com.tradeanalytics.stockanalysis/files/stocks/
   ```

### 方式2：应用内下载（开发中）

"下载数据"功能正在开发中，暂时需要手动准备数据。

## 数据格式

### 股票历史数据 (daily/*.csv)
每个CSV文件对应一只股票，文件名为股票代码（如`600000.csv`）

必需字段：
- `date`: 日期（YYYY-MM-DD）
- `code`: 股票代码
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量

### 股票列表 (stocks/stock_list.csv)
必需字段：
- `code`: 股票代码（6位数字）
- `name`: 股票名称

## 注意事项

1. **数据要求**
   - 每只股票至少需要10天以上的历史数据
   - 数据越多，分析越准确（建议150天以上）

2. **分析性能**
   - 分析所有股票可能需要几分钟时间
   - 处理过程中会显示进度
   - 请耐心等待分析完成

3. **结果解读**
   - 成交量倍数越高，表示资金关注度越高
   - 建议结合K线图和其他指标综合判断
   - 不构成投资建议，仅供参考

4. **存储空间**
   - 约5000只股票的数据需要约500MB空间
   - 请确保手机有足够的存储空间

## 常见问题

### Q: 为什么分析结果为空？
A: 可能原因：
- 数据目录中没有CSV文件
- 数据时间太旧，没有符合条件的股票
- 数据格式不正确

### Q: 如何更新数据？
A: 
- 目前需要在PC端下载最新数据后传输到手机
- 后续版本将支持应用内更新

### Q: 分析很慢怎么办？
A: 
- 这是正常现象，分析5000只股票需要2-5分钟
- 可以减少数据文件数量来加快分析速度

### Q: 如何查看之前的分析结果？
A: 
- 进入"历史记录"界面
- 所有分析结果都会自动保存
- 按时间倒序显示

## 版本历史

### v1.0.0 (当前版本)
- 完整的成交量分析功能
- 历史记录查看功能
- 中文字体支持
- 基础设置界面

## 技术支持

如有问题请参考：
- GitHub: https://github.com/zhouronghua/StockAnalysisAndroid
- 原项目: /home/ronghua.zhou/work/code/TradeAnalytics
