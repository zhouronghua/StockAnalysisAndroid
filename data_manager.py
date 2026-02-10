"""
Android应用数据管理模块
简化版，使用标准库，不依赖pandas
"""

import os
import glob
import csv
from datetime import datetime
from typing import List, Dict, Optional


class DataManager:
    """数据管理器"""
    
    def __init__(self, base_path: str):
        """
        初始化数据管理器
        
        Args:
            base_path: 基础路径
        """
        self.base_path = base_path
        self.daily_dir = os.path.join(base_path, 'daily')
        self.stocks_dir = os.path.join(base_path, 'stocks')
        self.results_dir = os.path.join(base_path, 'results')
        
        # 确保目录存在
        for dir_path in [self.daily_dir, self.stocks_dir, self.results_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def get_stock_list(self) -> List[Dict]:
        """获取股票列表"""
        stock_list_file = os.path.join(self.stocks_dir, 'stock_list.csv')
        
        if not os.path.exists(stock_list_file):
            return []
        
        try:
            stocks = []
            with open(stock_list_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    stocks.append(row)
            return stocks
        except Exception as e:
            print(f'读取股票列表失败: {e}')
            return []
    
    def get_stock_count(self) -> int:
        """获取股票数量"""
        csv_files = glob.glob(os.path.join(self.daily_dir, '*.csv'))
        return len(csv_files)
    
    def analyze_volume_surge(self, progress_callback=None) -> List[Dict]:
        """
        分析成交量暴涨股票
        
        Args:
            progress_callback: 进度回调函数(processed, total, found_count)
        
        Returns:
            分析结果列表
        """
        csv_files = glob.glob(os.path.join(self.daily_dir, '*.csv'))
        
        if not csv_files:
            return []
        
        all_results = []
        processed = 0
        total = len(csv_files)
        
        for file_path in csv_files:
            try:
                results = self._analyze_single_stock(file_path)
                if results:
                    all_results.extend(results)
                
                processed += 1
                
                if progress_callback and (processed % 100 == 0 or processed == total):
                    progress_callback(processed, total, len(all_results))
            
            except Exception as e:
                print(f'分析 {file_path} 失败: {e}')
                continue
        
        if not all_results:
            return []
        
        # 按日期排序，保留每只股票最新的记录
        all_results.sort(key=lambda x: x['date'], reverse=True)
        
        # 去重：只保留每只股票最新的记录
        seen_codes = set()
        unique_results = []
        for result in all_results:
            if result['stock_code'] not in seen_codes:
                unique_results.append(result)
                seen_codes.add(result['stock_code'])
        
        # 按成交量倍数排序
        unique_results.sort(key=lambda x: x['volume_ratio'], reverse=True)
        
        return unique_results
    
    def _analyze_single_stock(self, file_path: str) -> Optional[List[Dict]]:
        """
        分析单只股票
        
        Args:
            file_path: CSV文件路径
        
        Returns:
            符合条件的记录列表
        """
        try:
            # 读取CSV文件
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            if len(data) < 10:
                return None
            
            # 按日期排序
            data.sort(key=lambda x: x['date'])
            
            # 计算均线
            ma_period = self._get_ma_period(len(data))
            data = self._calculate_ma(data, ma_period)
            
            # 获取最近的数据
            recent_data = data[-min(10, len(data)):]
            
            results = []
            
            # 检查每一天（需要至少8天数据）
            for i in range(7, len(recent_data)):
                current = recent_data[i]
                
                # 跳过MA为None的数据
                if current.get('ma') is None:
                    continue
                
                # 计算前7天的平均成交量
                prev_7_days = recent_data[i-7:i]
                volumes = [float(d['volume']) for d in prev_7_days if d.get('volume')]
                
                if not volumes:
                    continue
                
                avg_7day_volume = sum(volumes) / len(volumes)
                current_volume = float(current['volume'])
                
                # 检查条件
                volume_ratio = current_volume / avg_7day_volume if avg_7day_volume > 0 else 0
                current_close = float(current['close'])
                current_ma = float(current['ma'])
                
                if volume_ratio >= 5.0 and current_close > current_ma:
                    stock_code = os.path.basename(file_path).replace('.csv', '')
                    stock_name = self._get_stock_name(stock_code)
                    
                    results.append({
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'date': current['date'],
                        'close': current_close,
                        'volume_ratio': volume_ratio,
                        'ma_period': ma_period
                    })
            
            return results
        
        except Exception as e:
            print(f'分析文件 {file_path} 失败: {e}')
            return None
    
    def _get_ma_period(self, data_length: int) -> int:
        """根据数据长度确定均线周期"""
        if data_length >= 120:
            return 120
        elif data_length >= 60:
            return 60
        elif data_length >= 30:
            return 30
        else:
            return 10
    
    def _calculate_ma(self, data: List[Dict], period: int) -> List[Dict]:
        """计算移动平均线"""
        for i in range(len(data)):
            if i < period - 1:
                data[i]['ma'] = None
            else:
                prices = [float(data[j]['close']) for j in range(i - period + 1, i + 1)]
                data[i]['ma'] = sum(prices) / len(prices)
        return data
    
    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        stock_list = self.get_stock_list()
        
        for stock in stock_list:
            if stock.get('code') == stock_code:
                return stock.get('name', stock_code)
        
        return stock_code
    
    def save_analysis_result(self, results: List[Dict]) -> str:
        """
        保存分析结果
        
        Args:
            results: 分析结果列表
        
        Returns:
            保存的文件路径
        """
        if not results:
            return ''
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'volume_analysis_{timestamp}.csv'
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                if results:
                    fieldnames = results[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
            return filepath
        except Exception as e:
            print(f'保存结果失败: {e}')
            return ''
    
    def get_history_files(self) -> List[Dict]:
        """获取历史分析结果文件列表"""
        result_files = glob.glob(os.path.join(self.results_dir, 'volume_analysis_*.csv'))
        result_files.sort(reverse=True)
        
        history = []
        for filepath in result_files:
            filename = os.path.basename(filepath)
            
            # 从文件名提取时间
            try:
                timestamp_str = filename.replace('volume_analysis_', '').replace('.csv', '')
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                date_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = filename
            
            # 读取文件获取记录数
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    count = sum(1 for row in reader) - 1  # 减去表头
            except:
                count = 0
            
            history.append({
                'filepath': filepath,
                'filename': filename,
                'date': date_str,
                'count': count
            })
        
        return history
    
    def load_history_result(self, filepath: str) -> List[Dict]:
        """加载历史分析结果"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            print(f'加载历史结果失败: {e}')
            return []
