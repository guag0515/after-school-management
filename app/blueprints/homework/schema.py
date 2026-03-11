from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class HomeworkBase(BaseModel):
    """作业基础信息"""
    student_id: int
    date: date
    chinese: Optional[str] = None
    math: Optional[str] = None
    english: Optional[str] = None
    science: Optional[str] = None
    other: Optional[str] = None
    completion_status: str
    teacher_evaluation: Optional[str] = None

class HomeworkCreate(HomeworkBase):
    """创建作业请求"""
    pass

class HomeworkUpdate(BaseModel):
    """更新作业请求"""
    chinese: Optional[str] = None
    math: Optional[str] = None
    english: Optional[str] = None
    science: Optional[str] = None
    other: Optional[str] = None
    completion_status: Optional[str] = None
    teacher_evaluation: Optional[str] = None

class HomeworkResponse(HomeworkBase):
    """作业响应"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True

class HomeworkListResponse(BaseModel):
    """作业列表响应"""
    total: int
    items: List[HomeworkResponse]
