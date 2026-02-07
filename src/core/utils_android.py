"""
安卓适配的工具函数模块
基于原utils.py，添加安卓路径支持
"""

import os
import logging
import configparser
from datetime import datetime, timedelta
from typing import Optional, List
import pandas as pd

# 检测平台
try:
    from kivy.utils import platform
    IS_ANDROID = (platform == 'android')
except:
    IS_ANDROID = False


def get_app_storage_path():
    """获取应用存储路径（兼容桌面和安卓）"""
    if IS_ANDROID:
        try:
            from android.storage import app_storage_path
            return app_storage_path()
        except:
            # 备用路径
            return '/storage/emulated/0/StockAnalysis'
    else:
        # 桌面环境
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def setup_directories():
    """创建必要的目录"""
    base_path = get_app_storage_path()
    
    paths = {
        'base': base_path,
        'data_dir': os.path.join(base_path, 'data'),
        'daily_dir': os.path.join(base_path, 'data', 'daily'),
        'stocks_dir': os.path.join(base_path, 'data', 'stocks'),
        'results_dir': os.path.join(base_path, 'data', 'results'),
        'logs_dir': os.path.join(base_path, 'logs'),
        'config_dir': os.path.join(base_path, 'config')
    }
    
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    
    return paths


class Config:
    """配置管理类（安卓适配）"""
    
    def __init__(self, config_file: str = 'config.ini'):
        self.config = configparser.ConfigParser()
        
        # 适配安卓路径
        if not os.path.isabs(config_file):
            base_path = get_app_storage_path()
            config_file = os.path.join(base_path, config_file)
        
        self.config_file = config_file
        
        if os.path.exists(config_file):
            self.config.read(config_file, encoding='utf-8')
        else:
            # 创建默认配置
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置文件"""
        paths = setup_directories()
        
        self.config['Paths'] = {
            'data_dir': paths['data_dir'],
            'daily_dir': paths['daily_dir'],
            'stocks_dir': paths['stocks_dir'],
            'results_dir': paths['results_dir'],
            'logs_dir': paths['logs_dir']
        }
        
        self.config['DataSource'] = {
            'source': 'baostock',
            'update_stock_list_days': '1'
        }
        
        self.config['Analysis'] = {
            'ma_period': '120',
            'volume_ratio_threshold': '5.0',
            'min_history_days': '150'
        }
        
        self.config['Scheduler'] = {
            'enabled': 'true',
            'run_time': '15:30',
            'weekdays_only': 'true'
        }
        
        self.config['Download'] = {
            'max_workers': '1',
            'retry_times': '3',
            'retry_delay': '5',
            'daily_download_limit_mb': '0'
        }
        
        # 保存配置
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get(self, section: str, key: str, fallback=None):
        """获取配置项"""
        return self.config.get(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback=None):
        """获取整数配置项"""
        return self.config.getint(section, key, fallback=fallback)
    
    def getfloat(self, section: str, key: str, fallback=None):
        """获取浮点数配置项"""
        return self.config.getfloat(section, key, fallback=fallback)
    
    def getboolean(self, section: str, key: str, fallback=None):
        """获取布尔配置项"""
        return self.config.getboolean(section, key, fallback=fallback)


def setup_logger(name: str, log_dir: str = None, level=logging.INFO) -> logging.Logger:
    """
    配置日志记录器（安卓适配）
    """
    if log_dir is None:
        log_dir = os.path.join(get_app_storage_path(), 'logs')
    
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        # 文件处理器
        log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 格式器
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def ensure_dir(directory: str):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)


def safe_read_csv(file_path: str, **kwargs) -> Optional[pd.DataFrame]:
    """安全读取CSV文件"""
    try:
        if not os.path.exists(file_path):
            return None
        return pd.read_csv(file_path, **kwargs)
    except Exception as e:
        logging.error(f"读取CSV失败: {file_path}, 错误: {e}")
        return None


def safe_write_csv(df: pd.DataFrame, file_path: str, **kwargs) -> bool:
    """安全写入CSV文件"""
    try:
        ensure_dir(os.path.dirname(file_path))
        df.to_csv(file_path, index=False, encoding='utf-8-sig', **kwargs)
        return True
    except Exception as e:
        logging.error(f"写入CSV失败: {file_path}, 错误: {e}")
        return False


def get_trading_days(start_date: datetime, end_date: datetime) -> List[datetime]:
    """获取交易日列表（简化版，排除周末）"""
    days = []
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # 周一到周五
            days.append(current)
        current += timedelta(days=1)
    return days


def format_date(date: datetime) -> str:
    """格式化日期为YYYY-MM-DD"""
    return date.strftime('%Y-%m-%d')


def parse_date(date_str: str) -> datetime:
    """解析日期字符串"""
    return datetime.strptime(date_str, '%Y-%m-%d')
