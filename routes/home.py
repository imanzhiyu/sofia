"""
FilePath: routes/home.py
Author: Joel
Date: 2025-07-31 22:53:32
LastEditTime: 2025-08-01 18:39:34
Description: 首页 & 统计
"""
from flask import Blueprint, render_template, request,send_file
from models.models import VisitStats
from datetime import datetime
from utils.get_client_ip import get_client_ip
from models import db
import os

home_bp = Blueprint('home', __name__)


@home_bp.before_app_request
def track_home_visit():
    if request.path != '/':
        return

    ip = get_client_ip()
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


@home_bp.route('/')
def index():
    total_visits = db.session.query(db.func.sum(VisitStats.visit_count)).scalar() or 0
    return render_template("index.html", total_visits=total_visits)
#检查用
@home_bp.route('/download_db')
def download_db():
    secret = request.args.get('key')
    if secret != 'Liyao123!!':
        return "Unauthorized", 403

    db_path = os.path.join(os.getcwd(), 'db', 'site.db')
    return send_file(db_path, as_attachment=True)
