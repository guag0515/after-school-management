from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class ScoreBase(BaseModel):
    """成绩基础信息"""
    student_id: int
    subject: str
    exam_type: str
    score: Decimal
    exam_time: date

class ScoreCreate(ScoreBase):
    """创建成绩请求"""
    pass

class ScoreUpdate(BaseModel):
    """更新成绩请求"""
    subject: Optional[str] = None
    exam_type: Optional[str] = None
    score: Optional[Decimal] = None
    exam_time: Optional[date] = None

class ScoreResponse(ScoreBase):
    """成绩响应"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True

class ScoreListResponse(BaseModel):
    """成绩列表响应"""
    total: int
    items: List[ScoreResponse]
