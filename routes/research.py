"""
FilePath: nature/personal_page/routes/research.py
Author: Joel
Date: 2025-07-31 22:53:42
LastEditTime: 2025-08-01 13:16:24
Description: 研究
"""
from flask import Blueprint, render_template
from models.models import Paper

research_bp = Blueprint('research', __name__)


@research_bp.route('/research')
def research():
    papers = Paper.query.order_by(Paper.year.desc()).all()
    paper_count = len(papers)
    return render_template('research.html', papers=papers, paper_count=paper_count)
