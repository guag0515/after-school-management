from flask import request
from app.blueprints.auth import auth_bp
from app.blueprints.auth.service import AuthService
from app.utils import success, error

@auth_bp.route('/login', methods=['POST'])
def login():
    """登录接口"""
    try:
        # 获取请求参数
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')
        
        # 验证参数
        if not username or not password or not user_type:
            return error(message="缺少必要参数")
        
        # 调用服务层进行登录验证
        result, msg = AuthService.login(username, password, user_type)
        if not result:
            return error(message=msg)
        
        # 返回登录成功响应
        return success(data=result.dict(), message="登录成功")
    except Exception as e:
        return error(message=str(e))
