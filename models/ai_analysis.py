from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class AIAnalysis(db.Model):
    __tablename__ = 'ai_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    analysis_period = Column(String(50), nullable=False)
    analysis_content = Column(Text, nullable=False)
    generate_time = Column(DateTime(timezone=True), server_default=func.now())
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 关系
    student = relationship('Student', back_populates='ai_analyses')
