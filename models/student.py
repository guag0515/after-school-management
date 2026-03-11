from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db

class Student(db.Model):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Integer, nullable=False)  # 0-女，1-男
    class_ = Column('class', String(50), nullable=False)
    service_type = Column(String(20), nullable=False)
    parent1_phone = Column(String(20), nullable=False)
    parent2_phone = Column(String(20))
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, default=0)
    
    # 关系
    parents = relationship('Parent', back_populates='student', cascade='all, delete-orphan')
    attendances = relationship('Attendance', back_populates='student', cascade='all, delete-orphan')
    homeworks = relationship('Homework', back_populates='student', cascade='all, delete-orphan')
    evaluations = relationship('Evaluation', back_populates='student', cascade='all, delete-orphan')
    scores = relationship('Score', back_populates='student', cascade='all, delete-orphan')
    meals = relationship('Meal', back_populates='student', cascade='all, delete-orphan')
    ai_analyses = relationship('AIAnalysis', back_populates='student', cascade='all, delete-orphan')
