"""
Android应用数据管理模块
简化版，适配移动端环境
"""

import os
import glob
import pandas as pd
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
            df = pd.read_csv(stock_list_file, dtype={'code': str})
            return df.to_dict('records')
        except Exception as e:
            print(f'读取股票列表失败: {e}')
            return []
    
    def get_stock_count(self) -> int:
        """获取股票数量"""
        csv_files = glob.glob(os.path.join(self.daily_dir, '*.csv'))
        return len(csv_files)
    
    def analyze_volume_surge(self, progress_callback=None) -> pd.DataFrame:
        """
        分析成交量暴涨股票
        
        Args:
            progress_callback: 进度回调函数
        
        Returns:
            分析结果DataFrame
        """
        csv_files = glob.glob(os.path.join(self.daily_dir, '*.csv'))
        
        if not csv_files:
            return pd.DataFrame()
        
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
            return pd.DataFrame()
        
        # 转换为DataFrame并排序
        results_df = pd.DataFrame(all_results)
        results_df['date'] = pd.to_datetime(results_df['date'])
        results_df = results_df.sort_values('date', ascending=False)
        results_df = results_df.drop_duplicates(subset='stock_code', keep='first')
        results_df['date'] = results_df['date'].dt.strftime('%Y-%m-%d')
        results_df = results_df.sort_values('volume_ratio', ascending=False)
        
        return results_df
    
    def _analyze_single_stock(self, file_path: str) -> Optional[List[Dict]]:
        """
        分析单只股票
        
        Args:
            file_path: CSV文件路径
        
        Returns:
            符合条件的记录列表
        """
        try:
            df = pd.read_csv(file_path, dtype={'code': str})
            
            if len(df) < 10:
                return None
            
            # 确保日期排序
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 计算均线
            if len(df) >= 120:
                ma_period = 120
            elif len(df) >= 60:
                ma_period = 60
            elif len(df) >= 30:
                ma_period = 30
            else:
                ma_period = 10
            
            df['ma'] = df['close'].rolling(window=ma_period).mean()
            
            # 获取最近的数据
            recent_data = df.tail(min(10, len(df)))
            
            results = []
            
            # 检查每一天
            for i in range(7, len(recent_data)):
                current = recent_data.iloc[i]
                
                if pd.isna(current['ma']):
                    continue
                
                # 计算前7天的平均成交量
                prev_7_days = recent_data.iloc[i-7:i]
                avg_7day_volume = prev_7_days['volume'].mean()
                
                # 检查条件：当天成交量是前7天平均成交量的5倍以上
                volume_ratio = current['volume'] / avg_7day_volume if avg_7day_volume > 0 else 0
                
                if volume_ratio >= 5.0 and current['close'] > current['ma']:
                    stock_code = os.path.basename(file_path).replace('.csv', '')
                    stock_name = self._get_stock_name(stock_code)
                    
                    results.append({
                        'stock_code': stock_code,
                        'stock_name': stock_name,
                        'date': current['date'].strftime('%Y-%m-%d'),
                        'close': float(current['close']),
                        'volume_ratio': float(volume_ratio),
                        'ma_period': ma_period
                    })
            
            return results
        
        except Exception as e:
            return None
    
    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        stock_list = self.get_stock_list()
        
        for stock in stock_list:
            if stock.get('code') == stock_code:
                return stock.get('name', stock_code)
        
        return stock_code
    
    def save_analysis_result(self, results_df: pd.DataFrame) -> str:
        """
        保存分析结果
        
        Args:
            results_df: 分析结果DataFrame
        
        Returns:
            保存的文件路径
        """
        if results_df.empty:
            return ''
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'volume_analysis_{timestamp}.csv'
        filepath = os.path.join(self.results_dir, filename)
        
        try:
            results_df.to_csv(filepath, index=False, encoding='utf-8-sig')
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
                df = pd.read_csv(filepath)
                count = len(df)
            except:
                count = 0
            
            history.append({
                'filepath': filepath,
                'filename': filename,
                'date': date_str,
                'count': count
            })
        
        return history
    
    def load_history_result(self, filepath: str) -> pd.DataFrame:
        """加载历史分析结果"""
        try:
            return pd.read_csv(filepath, dtype={'stock_code': str})
        except Exception as e:
            print(f'加载历史结果失败: {e}')
            return pd.DataFrame()
