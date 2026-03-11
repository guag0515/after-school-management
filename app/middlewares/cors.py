from flask import Flask
from flask_cors import CORS

def init_cors(app: Flask):
    """初始化CORS"""
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
