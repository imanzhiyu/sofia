"""
FilePath: nature/personal_page/routes/cv.py
Author: Joel
Date: 2025-07-31 22:53:59
LastEditTime: 2025-07-31 23:00:28
Description: 简历
"""
from flask import Blueprint, render_template

cv_bp = Blueprint('cv', __name__)


@cv_bp.route('/cv')
def cv():
    return render_template('cv.html')
