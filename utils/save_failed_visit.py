"""
FilePath: utils/save_failed_visit.py
Author: Joel
Date: 2025-08-02 19:03:39
LastEditTime: 2025-08-02 19:07:18
Description: 补录访客
"""
from datetime import datetime
import json
import os

CACHE_FILE = os.path.join('static','data','failed_visits.json')
def save_failed_visit(ip):
    data = {'ip': ip, 'timestamp': datetime.utcnow().isoformat()}
    try:
        # 加到列表中
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
        else:
            cache = []

        cache.append(data)

        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"写入缓存失败: {e}")
