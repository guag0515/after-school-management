from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Score(db.Model):
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject = Column(String(50), nullable=False)
    exam_type = Column(String(50), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    exam_time = Column(Date, nullable=False)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 关系
    student = relationship('Student', back_populates='scores')
