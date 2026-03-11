from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    is_present = Column(Integer, nullable=False)  # 0-未到校，1-到校
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 唯一约束
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='uk_student_date'),
    )
    
    # 关系
    student = relationship('Student', back_populates='attendances')
