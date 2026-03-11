from flask import Flask
from app.config import Config
from app.extensions import db, jwt
from app.middlewares import init_cors

# 导入蓝图
from app.blueprints.auth import auth_bp
from app.blueprints.student import student_bp
from app.blueprints.attendance import attendance_bp
from app.blueprints.homework import homework_bp
from app.blueprints.score import score_bp
from app.blueprints.meal import meal_bp
from app.blueprints.ai_analysis import ai_analysis_bp
from app.blueprints.admin import admin_bp

# 导入模型
from app.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    
    # 初始化CORS
    init_cors(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(homework_bp, url_prefix='/api/homework')
    app.register_blueprint(score_bp, url_prefix='/api/scores')
    app.register_blueprint(meal_bp, url_prefix='/api/meals')
    app.register_blueprint(ai_analysis_bp, url_prefix='/api/ai-analysis')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app
