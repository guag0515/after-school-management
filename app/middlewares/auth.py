from flask import request, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.utils import unauthorized, forbidden
from app.models import Parent, Student

def auth_required():
    """认证中间件"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                # 验证JWT令牌
                verify_jwt_in_request()
                # 获取用户信息
                identity = get_jwt_identity()
                g.user_id = identity.get('user_id')
                g.user_type = identity.get('user_type')
                return f(*args, **kwargs)
            except Exception as e:
                return unauthorized("请先登录")
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

def admin_required():
    """管理员权限中间件"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                # 验证JWT令牌
                verify_jwt_in_request()
                # 获取用户信息
                identity = get_jwt_identity()
                user_type = identity.get('user_type')
                if user_type != 'admin':
                    return forbidden("需要管理员权限")
                g.user_id = identity.get('user_id')
                g.user_type = user_type
                return f(*args, **kwargs)
            except Exception as e:
                return unauthorized("请先登录")
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

def parent_required():
    """家长权限中间件"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                # 验证JWT令牌
                verify_jwt_in_request()
                # 获取用户信息
                identity = get_jwt_identity()
                user_type = identity.get('user_type')
                if user_type != 'parent':
                    return forbidden("需要家长权限")
                g.user_id = identity.get('user_id')
                g.user_type = user_type
                return f(*args, **kwargs)
            except Exception as e:
                return unauthorized("请先登录")
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

def check_student_permission(student_id):
    """检查家长是否有权限访问学生数据"""
    # 获取当前用户
    user_id = g.user_id
    user_type = g.user_type
    
    # 管理员可以访问所有学生数据
    if user_type == 'admin':
        return True
    
    # 家长只能访问自己孩子的数据
    if user_type == 'parent':
        parent = Parent.query.get(user_id)
        if parent and parent.student_id == student_id:
            return True
    
    return False
