from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class StudentBase(BaseModel):
    """学生基础信息"""
    name: str
    gender: int
    class_: str
    service_type: str
    parent1_phone: str
    parent2_phone: Optional[str] = None

class StudentCreate(StudentBase):
    """创建学生请求"""
    pass

class StudentUpdate(BaseModel):
    """更新学生请求"""
    name: Optional[str] = None
    gender: Optional[int] = None
    class_: Optional[str] = None
    service_type: Optional[str] = None
    parent1_phone: Optional[str] = None
    parent2_phone: Optional[str] = None

class StudentResponse(StudentBase):
    """学生响应"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class StudentListResponse(BaseModel):
    """学生列表响应"""
    total: int
    items: List[StudentResponse]

class ParentCreate(BaseModel):
    """创建家长请求"""
    student_id: int
    phone: str
    password: str
    relation: str
