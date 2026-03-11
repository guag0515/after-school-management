from datetime import datetime
from app.extensions import db

class Homework(db.Model):
    __tablename__ = 'homework'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    chinese = db.Column(db.Text)
    math = db.Column(db.Text)
    english = db.Column(db.Text)
    science = db.Column(db.Text)
    other = db.Column(db.Text)
    completion_status = db.Column(db.String(20), default='pending')
    teacher_evaluation = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
