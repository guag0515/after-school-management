from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    evaluation_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    evaluation_date = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey('admins.id', ondelete='CASCADE'), nullable=False)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 关系
    student = relationship('Student', back_populates='evaluations')
    teacher = relationship('Admin', back_populates='evaluations')
