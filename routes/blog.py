"""
FilePath: nature/personal_page/routes/blog.py
Author: Joel
Date: 2025-07-31 22:53:51
LastEditTime: 2025-07-31 23:09:24
Description: 博客列表与详情
"""
from flask import Blueprint, render_template, abort
import os
from utils.markdown_parser import parse_markdown

blog_bp = Blueprint('blog', __name__)

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'posts')


@blog_bp.route('/blog')
def blog():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            path = os.path.join(POSTS_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                html, meta = parse_markdown(content, return_meta=True)
                posts.append({
                    'title': meta.get('title', 'Untitled'),
                    'date': meta.get('date', 'Unknown Date'),
                    'summary': meta.get('summary', ''),
                    'filename': filename.replace('.md', '')
                })
    posts.sort(key=lambda x: x['date'], reverse=True)
    return render_template('blog.html', posts=posts)


@blog_bp.route('/blog/<slug>')
def blog_post(slug):
    filepath = os.path.join(POSTS_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        html, meta = parse_markdown(content, return_meta=True)
    return render_template('blog_post.html', title=meta.get('title', 'Blog'), date=meta.get('date', ''), content=html)
