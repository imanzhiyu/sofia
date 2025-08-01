"""
FilePath: models/models.py
Author: Joel
Date: 2025-07-31 19:12:39
LastEditTime: 2025-08-01 20:25:06
Description: 数据库结构和模型设计
"""
from datetime import datetime, timedelta
from . import db


class VisitStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), unique=True, nullable=False)
    visit_count = db.Column(db.Integer, default=1)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)

    def is_recent(self, window_minutes=3):
        return datetime.utcnow() - self.last_visit < timedelta(minutes=window_minutes)


class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    authors = db.Column(db.String(512), nullable=False)
    year = db.Column(db.String(10))
    journal = db.Column(db.String(512))
    url = db.Column(db.String(512))
    is_first_author = db.Column(db.Boolean, default=False)
