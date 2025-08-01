"""
FilePath: nature/personal_page/utils/markdown_parser.py
Author: Joel
Date: 2025-07-30 15:07:52
LastEditTime: 2025-07-30 17:56:13
Description:  解析Markdown为HTML
"""
import markdown
import re


def parse_markdown(content, return_meta=False):
    # 使用正则提取元信息
    meta = {}
    meta_match = re.findall(r'^(\w+):\s*(.+)$', content, re.MULTILINE)
    for key, value in meta_match:
        meta[key.lower()] = value.strip()

    # 去除 meta 再转 HTML
    content_without_meta = re.sub(r'^(\w+):\s*(.+)$', '', content, flags=re.MULTILINE).strip()
    html = markdown.markdown(content_without_meta, extensions=['fenced_code', 'codehilite'])

    if return_meta:
        return html, meta
    return html
