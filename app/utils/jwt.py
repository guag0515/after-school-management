from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from flask import request, jsonify
import datetime

def generate_token(user_id, user_type):
    """生成JWT令牌"""
    # 设置过期时间为1小时
    expires = datetime.timedelta(hours=1)
    # 创建访问令牌，包含用户ID和用户类型
    access_token = create_access_token(
        identity={"user_id": user_id, "user_type": user_type}, 
        expires_delta=expires
    )
    return access_token

def get_current_user():
    """获取当前用户信息"""
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        return identity
    except Exception as e:
        return None

def get_current_user_id():
    """获取当前用户ID"""
    user = get_current_user()
    if user:
        return user.get("user_id")
    return None

def get_current_user_type():
    """获取当前用户类型"""
    user = get_current_user()
    if user:
        return user.get("user_type")
    return None
