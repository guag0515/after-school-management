from datetime import datetime
from app.extensions import db

class Score(db.Model):
    __tablename__ = 'score'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    exam_date = db.Column(db.Date, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
