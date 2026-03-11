from app.models import Admin, Parent
from app.utils import verify_password, generate_token
from app.blueprints.auth.schema import LoginResponse

class AuthService:
    @staticmethod
    def login(username, password, user_type):
        """登录验证"""
        if user_type == 'admin':
            # 管理员登录
            admin = Admin.query.filter_by(username=username, is_deleted=0).first()
            if not admin:
                return None, "管理员不存在"
            if not verify_password(password, admin.password):
                return None, "密码错误"
            # 生成token
            access_token = generate_token(admin.id, 'admin')
            return LoginResponse(
                access_token=access_token,
                user_type='admin',
                user_id=admin.id,
                name=admin.name
            ), None
        elif user_type == 'parent':
            # 家长登录
            parent = Parent.query.filter_by(phone=username, is_deleted=0).first()
            if not parent:
                return None, "家长不存在"
            if not verify_password(password, parent.password):
                return None, "密码错误"
            # 生成token
            access_token = generate_token(parent.id, 'parent')
            return LoginResponse(
                access_token=access_token,
                user_type='parent',
                user_id=parent.id,
                name=f"{parent.student.name}的{parent.relation}"
            ), None
        else:
            return None, "用户类型错误"
