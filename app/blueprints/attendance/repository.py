from sqlalchemy.orm import Session
from app.models import Attendance
from app.blueprints.attendance.schema import AttendanceCreate, AttendanceUpdate

class AttendanceRepository:
    @staticmethod
    def create(db: Session, attendance_data: AttendanceCreate) -> Attendance:
        """创建考勤"""
        db_attendance = Attendance(
            student_id=attendance_data.student_id,
            date=attendance_data.date,
            is_present=attendance_data.is_present
        )
        db.add(db_attendance)
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
    
    @staticmethod
    def get_by_id(db: Session, attendance_id: int) -> Attendance:
        """根据ID获取考勤"""
        return db.query(Attendance).filter(Attendance.id == attendance_id, Attendance.is_deleted == 0).first()
    
    @staticmethod
    def get_by_student_and_date(db: Session, student_id: int, date: str) -> Attendance:
        """根据学生ID和日期获取考勤"""
        return db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date == date,
            Attendance.is_deleted == 0
        ).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取考勤列表"""
        query = db.query(Attendance).filter(Attendance.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('student_id'):
            query = query.filter(Attendance.student_id == filters['student_id'])
        if filters.get('date_from'):
            query = query.filter(Attendance.date >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Attendance.date <= filters['date_to'])
        if filters.get('is_present') is not None:
            query = query.filter(Attendance.is_present == filters['is_present'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def update(db: Session, attendance_id: int, attendance_data: AttendanceUpdate) -> Attendance:
        """更新考勤"""
        db_attendance = AttendanceRepository.get_by_id(db, attendance_id)
        if db_attendance:
            update_data = attendance_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_attendance, field, value)
            db.commit()
            db.refresh(db_attendance)
        return db_attendance
    
    @staticmethod
    def delete(db: Session, attendance_id: int) -> bool:
        """删除考勤（软删除）"""
        db_attendance = AttendanceRepository.get_by_id(db, attendance_id)
        if db_attendance:
            db_attendance.is_deleted = 1
            db.commit()
            return True
        return False
