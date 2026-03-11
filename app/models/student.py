from datetime import datetime
from app.extensions import db

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    school_class = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(20), nullable=False)
    parent1_phone = db.Column(db.String(20), nullable=False)
    parent2_phone = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
