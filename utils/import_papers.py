"""
FilePath: nature/personal_page/utils/import_papers.py
Author: Joel
Date: 2025-08-01 12:44:07
LastEditTime: 2025-08-01 13:10:04
Description: 插入数据脚本
"""
from models.models import db, Paper
from data.papers import papers


def import_papers():
    for paper in papers:
        # 通过标题识别
        existing_paper = Paper.query.filter_by(title=paper['title']).first()
        if existing_paper:
            # 更新已存在记录
            existing_paper.authors = paper['authors']
            existing_paper.year = paper['year']
            existing_paper.journal = paper['journal']
            existing_paper.url = paper['url']
            existing_paper.is_first_author = paper['is_first_author']
        else:
            # 新增记录
            new_paper = Paper(
                title=paper['title'],
                authors=paper['authors'],
                year=paper['year'],
                journal=paper['journal'],
                url=paper['url'],
                is_first_author=paper['is_first_author']
            )
            db.session.add(new_paper)
    db.session.commit()
