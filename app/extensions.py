from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# 初始化SQLAlchemy
db = SQLAlchemy()

# 初始化JWT
jwt = JWTManager()
