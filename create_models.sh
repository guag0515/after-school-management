#!/bin/bash

# 创建models目录
mkdir -p /opt/after-school-management/code/app/models

# 创建__init__.py文件
cat > /opt/after-school-management/code/app/models/__init__.py << 'EOF'
from .admin import Admin
from .parent import Parent
from .student import Student
from .attendance import Attendance
from .homework import Homework
from .score import Score
from .meal import Meal
from .ai_analysis import AIAnalysis
from .evaluation import Evaluation
EOF

# 创建admin.py文件
cat > /opt/after-school-management/code/app/models/admin.py << 'EOF'
from datetime import datetime
from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='teacher')
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
EOF

# 创建parent.py文件
cat > /opt/after-school-management/code/app/models/parent.py << 'EOF'
from datetime import datetime
from app.extensions import db

class Parent(db.Model):
    __tablename__ = 'parent'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    relationship = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
EOF

# 创建student.py文件
cat > /opt/after-school-management/code/app/models/student.py << 'EOF'
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
EOF

# 创建attendance.py文件
cat > /opt/after-school-management/code/app/models/attendance.py << 'EOF'
from datetime import datetime
from app.extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_present = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
EOF

# 创建homework.py文件
cat > /opt/after-school-management/code/app/models/homework.py << 'EOF'
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
EOF

# 创建score.py文件
cat > /opt/after-school-management/code/app/models/score.py << 'EOF'
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
EOF

# 创建meal.py文件
cat > /opt/after-school-management/code/app/models/meal.py << 'EOF'
from datetime import datetime
from app.extensions import db

class Meal(db.Model):
    __tablename__ = 'meal'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    breakfast = db.Column(db.String(2