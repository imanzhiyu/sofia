"""
FilePath: app.py
Author: Joel
Date: 2025-07-30 14:31:06
LastEditTime: 2025-08-02 18:39:13
Description: Flask
"""

from flask import Flask
from models import db
from routes import home_bp, research_bp, blog_bp, cv_bp
import os
from utils.import_papers import import_papers
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # db_dir = os.path.join(basedir, 'db')
    # os.makedirs(db_dir, exist_ok=True)
    load_dotenv()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    #'sqlite:///' + os.path.join(db_dir, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #防止 SSL connection closed
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True
    }
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # 插入paper数据
        import_papers()

    app.register_blueprint(home_bp)
    app.register_blueprint(research_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(cv_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
