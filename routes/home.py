"""
FilePath: nature/personal_page/routes/home.py
Author: Joel
Date: 2025-07-31 22:53:32
LastEditTime: 2025-07-31 23:05:05
Description: 首页 & 统计
"""
from flask import Blueprint, render_template, request
from models.models import VisitStats
from datetime import datetime
from utils.get_client_ip import get_client_ip
from models import db

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
