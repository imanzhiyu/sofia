"""
FilePath: nature/personal_page/routes/__init__.py
Author: Joel
Date: 2025-07-31 22:53:25
LastEditTime: 2025-07-31 23:05:45
Description: 
"""
from .home import home_bp
from .research import research_bp
from .blog import blog_bp
from .cv import cv_bp

__all__ = ['home_bp', 'research_bp', 'blog_bp', 'cv_bp']
