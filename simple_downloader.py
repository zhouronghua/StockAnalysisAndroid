"""
简化的数据下载器
使用公开API，不依赖pandas和baostock
"""

import os
import csv
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable


class SimpleDownloader:
    """简化的数据下载器"""
    
    def __init__(self, base_path: str):
        """
        初始化下载器
        
        Args:
            base_path: 基础路径
        """
        self.base_path = base_path
        self.daily_dir = os.path.join(base_path, 'daily')
        self.stocks_dir = os.path.join(base_path, 'stocks')
        
        # 确保目录存在
        os.makedirs(self.daily_dir, exist_ok=True)
        os.makedirs(self.stocks_dir, exist_ok=True)
        
        # 使用新浪财经接口（免费，无需密钥）
        self.base_url = "http://hq.sinajs.cn/list="
        
        # 东方财富网接口（备用）
        self.eastmoney_url = "http://push2.eastmoney.com/api/qt/stock/kline/get"
    
    def get_stock_list(self, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        获取股票列表
        使用预定义的主要股票代码
        
        Args:
            progress_callback: 进度回调
        
        Returns:
            股票列表
        """
        stock_list = []
        
        # 主要指数和热门股票
        stocks = [
            # 上证指数成分股（部分）
            ('sh600000', '浦发银行'),
            ('sh600004', '白云机场'),
            ('sh600009', '上海机场'),
            ('sh600016', '民生银行'),
            ('sh600019', '宝钢股份'),
            ('sh600028', '中国石化'),
            ('sh600030', '中信证券'),
            ('sh600036', '招商银行'),
            ('sh600048', '保利发展'),
            ('sh600050', '中国联通'),
            
            # 深证成分股（部分）
            ('sz000001', '平安银行'),
            ('sz000002', '万科A'),
            ('sz000063', '中兴通讯'),
            ('sz000100', 'TCL科技'),
            ('sz000333', '美的集团'),
            ('sz000338', '潍柴动力'),
            ('sz000651', '格力电器'),
            ('sz000858', '五粮液'),
            
            # 创业板（部分）
            ('sz300059', '东方财富'),
            ('sz300124', '汇川技术'),
            ('sz300142', '沃森生物'),
            ('sz300750', '宁德时代'),
        ]
        
        for code, name in stocks:
            stock_list.append({
                'code': code[2:],  # 去掉sh/sz前缀
                'name': name,
                'exchange': code[:2]
            })
            
            if progress_callback:
                progress_callback(len(stock_list), len(stocks), 0)
        
        # 保存股票列表
        self._save_stock_list(stock_list)
        
        return stock_list
    
    def _save_stock_list(self, stock_list: List[Dict]):
        """保存股票列表到CSV"""
        filepath = os.path.join(self.stocks_dir, 'stock_list.csv')
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['code', 'name', 'exchange'])
            writer.writeheader()
            for stock in stock_list:
                writer.writerow({
                    'code': stock['code'],
                    'name': stock['name'],
                    'exchange': stock.get('exchange', 'sh')
                })
    
    def download_stock_history(self, stock_code: str, exchange: str = 'sh',
                               days: int = 180,
                               progress_callback: Optional[Callable] = None) -> bool:
        """
        下载单只股票的历史数据
        
        Args:
            stock_code: 股票代码（6位）
            exchange: 交易所（sh/sz）
            days: 历史天数
            progress_callback: 进度回调
        
        Returns:
            是否成功
        """
        try:
            # 使用东方财富网接口
            full_code = f"0.{stock_code}" if exchange == 'sz' else f"1.{stock_code}"
            
            params = {
                'secid': full_code,
                'fields1': 'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt': '101',  # 日K
                'fqt': '1',    # 前复权
                'beg': (datetime.now() - timedelta(days=days)).strftime('%Y%m%d'),
                'end': datetime.now().strftime('%Y%m%d'),
            }
            
            response = requests.get(self.eastmoney_url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f'下载失败: {stock_code}, 状态码 {response.status_code}')
                return False
            
            data = response.json()
            
            if data['rc'] != 0 or not data.get('data'):
                print(f'无数据: {stock_code}')
                return False
            
            klines = data['data']['klines']
            
            if not klines:
                print(f'无K线数据: {stock_code}')
                return False
            
            # 保存为CSV
            filepath = os.path.join(self.daily_dir, f'{stock_code}.csv')
            
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['date', 'code', 'open', 'high', 'low', 'close', 'volume', 'amount', 'turn'])
                
                # 写入数据
                for kline in klines:
                    parts = kline.split(',')
                    if len(parts) >= 9:
                        writer.writerow([
                            parts[0],      # 日期
                            stock_code,    # 代码
                            parts[1],      # 开盘
                            parts[2],      # 最高
                            parts[3],      # 最低
                            parts[4],      # 收盘
                            parts[5],      # 成交量
                            parts[6],      # 成交额
                            parts[8],      # 换手率
                        ])
            
            return True
        
        except Exception as e:
            print(f'下载 {stock_code} 失败: {e}')
            return False
    
    def download_all_stocks(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        下载所有股票数据
        
        Args:
            progress_callback: 进度回调(current, total, success_count)
        
        Returns:
            下载统计信息
        """
        # 先获取股票列表
        stock_list = self.get_stock_list()
        
        total = len(stock_list)
        success = 0
        failed = 0
        
        for i, stock in enumerate(stock_list):
            code = stock['code']
            exchange = stock.get('exchange', 'sh')
            
            if self.download_stock_history(code, exchange):
                success += 1
            else:
                failed += 1
            
            # 进度回调
            if progress_callback:
                progress_callback(i + 1, total, success)
            
            # 避免请求过快
            time.sleep(0.5)
        
        return {
            'total': total,
            'success': success,
            'failed': failed
        }
    
    def update_single_stock(self, stock_code: str, exchange: str = 'sh') -> bool:
        """
        更新单只股票的数据（只下载最新数据）
        
        Args:
            stock_code: 股票代码
            exchange: 交易所
        
        Returns:
            是否成功
        """
        # 检查现有文件
        filepath = os.path.join(self.daily_dir, f'{stock_code}.csv')
        
        if os.path.exists(filepath):
            # 读取最后日期
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = list(csv.reader(f))
                    if len(lines) > 1:
                        last_date = lines[-1][0]
                        last_date_obj = datetime.strptime(last_date, '%Y-%m-%d')
                        days_diff = (datetime.now() - last_date_obj).days
                        
                        if days_diff <= 1:
                            # 数据已是最新
                            return True
            except:
                pass
        
        # 下载数据
        return self.download_stock_history(stock_code, exchange, days=30)
