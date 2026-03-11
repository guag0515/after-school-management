from datetime import datetime
from app.extensions import db

class Meal(db.Model):
    __tablename__ = 'meal'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    breakfast = db.Column(db.String(255))
    lunch = db.Column(db.String(255))
    dinner = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
