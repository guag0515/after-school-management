import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql://root:password@localhost:3306/asm_system')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
    
    # 其他配置
    DEBUG = os.getenv('DEBUG', True)
