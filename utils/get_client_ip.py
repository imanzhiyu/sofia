"""
FilePath: nature/personal_page/utils/get_client_ip.py
Author: Joel
Date: 2025-07-31 19:26:27
LastEditTime: 2025-07-31 19:26:54
Description: 获取用户真是IP
"""

from flask import request


def get_client_ip():
    """获取用户真实 IP 地址"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip
