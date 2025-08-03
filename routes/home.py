"""
FilePath: routes/home.py
Author: Joel
Date: 2025-07-31 22:53:32
LastEditTime: 2025-08-03 21:00:14
Description: 首页 & 统计
"""
import json

from flask import Blueprint, render_template, request,send_file
from models.models import VisitStats
from datetime import datetime,timedelta
from utils.get_client_ip import get_client_ip
from models import db
from utils.save_failed_visit import save_failed_visit
import os

home_bp = Blueprint('home', __name__)


@home_bp.before_app_request
def track_home_visit():
    if request.path != '/':
        return
    ip = get_client_ip()
    try:
        stat = VisitStats.query.filter_by(ip=ip).first()
        if stat:
            if not stat.is_recent():
                stat.visit_count += 1
                stat.last_visit = datetime.utcnow()
                db.session.commit()
        else:
            new_stat = VisitStats(ip=ip)
            db.session.add(new_stat)
            db.session.commit()
    except Exception as e:
        save_failed_visit(ip)
        # 避免数据库断连造成首页 500
        print(f"[ERROR] Failed to track visit for IP {ip if 'ip' in locals() else 'unknown'}: {e}")



@home_bp.route('/')
def index():
    update_last_visit()
    total_visits = db.session.query(db.func.sum(VisitStats.visit_count)).scalar() or 0
    return render_template("index.html", total_visits=total_visits)

CACHE_FILE = os.path.join('static','data','failed_visits.json')
@home_bp.route('/recover_failed_visits')
def recover_failed_visits():
    secret = request.args.get('key')
    if secret != 'Liyao123!!':
        return "Unauthorized", 403

    if not os.path.exists(CACHE_FILE):
        return "No failed visits to recover"

    with open(CACHE_FILE, 'r') as f:
        visits = json.load(f)

    success = 0
    for visit in visits:
        ip = visit['ip']
        timestamp = datetime.fromisoformat(visit['timestamp'])
        try:
            stat = VisitStats.query.filter_by(ip=ip).first()
            if stat:
                if (timestamp - stat.last_visit).total_seconds() > 60:
                    stat.visit_count += 1
                    stat.last_visit = timestamp
            else:
                new_stat = VisitStats(ip=ip, visit_count=1, last_visit=timestamp)
                db.session.add(new_stat)
            db.session.commit()
            success += 1
        except Exception as e:
            print(f"[ERROR] 恢复失败: {e}")

    # 清空文件
    if success > 0:
        with open(CACHE_FILE, 'w') as f:
            json.dump([], f)

    return f"{success} visits recovered"

#ping
path = os.path.join('static','data', 'last_visit.txt')
# 读取上次访问时间
def read_last_visit():
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        try:
            return datetime.fromisoformat(f.read().strip())
        except:
            return None
#更新上次访问时间
def update_last_visit():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(datetime.utcnow().isoformat())
@home_bp.route('/ping')
def ping():
    secret = request.args.get('key')
    if secret != 'Liyao123!!':
        return "Unauthorized", 403
    
    last_visit = read_last_visit()
    now = datetime.utcnow()
    if last_visit is None or (now - last_visit) > timedelta(minutes=13.5):
        update_last_visit()
        return 'pong', 200
    return f'Not needed({last_visit})', 200
#检查用
@home_bp.route('/download_db')
def download_db():
    secret = request.args.get('key')
    if secret != 'Liyao123!!':
        return "Unauthorized", 403

    db_path = os.path.join(os.getcwd(), 'db', 'site.db')
    return send_file(db_path, as_attachment=True)
