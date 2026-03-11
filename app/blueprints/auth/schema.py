from pydantic import BaseModel

class LoginRequest(BaseModel):
    """登录请求"""
    username: str
    password: str
    user_type: str

class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str
    user_type: str
    user_id: int
    name: str
