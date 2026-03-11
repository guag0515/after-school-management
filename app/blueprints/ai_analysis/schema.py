from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AIAnalysisBase(BaseModel):
    """AI分析基础信息"""
    student_id: int
    analysis_period: str
    analysis_content: str

class AIAnalysisCreate(AIAnalysisBase):
    """创建AI分析请求"""
    pass

class AIAnalysisResponse(AIAnalysisBase):
    """AI分析响应"""
    id: int
    generate_time: datetime
    create_time: datetime
    update_time: datetime
    
    class Config:
        orm_mode = True

class AIAnalysisListResponse(BaseModel):
    """AI分析列表响应"""
    total: int
    items: List[AIAnalysisResponse]
