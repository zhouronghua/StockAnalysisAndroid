"""
安卓后台服务
用于定时任务
"""

from time import sleep
import os

# 保持服务运行
print("Stock Analysis Service Started")

while True:
    # 每小时检查一次
    sleep(3600)
    print("Service running...")
