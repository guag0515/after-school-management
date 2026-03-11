from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Parent(db.Model):
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    relation = Column(String(20), nullable=False)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 关系
    student = relationship('Student', back_populates='parents')
