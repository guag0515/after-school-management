from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class MealBase(BaseModel):
    """餐饮基础信息"""
    student_id: int
    date: date
    breakfast: Optional[str] = None
    lunch: Optional[str] = None
    dinner: Optional[str] = None

class MealCreate(MealBase):
    """创建餐饮请求"""
    pass

class MealUpdate(BaseModel):
    """更新餐饮请求"""
    breakfast: Optional[str] = None
    lunch: Optional[str] = None
    dinner: Optional[str] = None

class MealResponse(MealBase):
    """餐饮响应"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True

class MealListResponse(BaseModel):
    """餐饮列表响应"""
    total: int
    items: List[MealResponse]
