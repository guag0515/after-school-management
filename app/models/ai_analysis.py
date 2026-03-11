from datetime import datetime
from app.extensions import db

class AIAnalysis(db.Model):
    __tablename__ = 'ai_analysis'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    analysis_period = db.Column(db.String(20), nullable=False)
    analysis_content = db.Column(db.Text, nullable=False)
    generate_time = db.Column(db.DateTime, default=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
