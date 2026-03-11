from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Homework(db.Model):
    __tablename__ = 'homework'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    chinese = Column(Text)
    math = Column(Text)
    english = Column(Text)
    science = Column(Text)
    other = Column(Text)
    completion_status = Column(String(20), nullable=False)
    teacher_evaluation = Column(Text)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 唯一约束
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='uk_student_date'),
    )
    
    # 关系
    student = relationship('Student', back_populates='homeworks')
