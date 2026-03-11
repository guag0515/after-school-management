from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class AttendanceBase(BaseModel):
    """考勤基础信息"""
    student_id: int
    date: date
    is_present: int

class AttendanceCreate(AttendanceBase):
    """创建考勤请求"""
    pass

class AttendanceUpdate(BaseModel):
    """更新考勤请求"""
    is_present: Optional[int] = None

class AttendanceResponse(AttendanceBase):
    """考勤响应"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True

class AttendanceListResponse(BaseModel):
    """考勤列表响应"""
    total: int
    items: List[AttendanceResponse]
