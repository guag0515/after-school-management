from sqlalchemy.orm import Session
from app.blueprints.attendance.repository import AttendanceRepository
from app.blueprints.attendance.schema import AttendanceCreate, AttendanceUpdate
from app.models import Attendance
from app.blueprints.student.repository import StudentRepository

class AttendanceService:
    @staticmethod
    def create_attendance(db: Session, attendance_data: AttendanceCreate) -> Attendance:
        """创建考勤"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, attendance_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 检查是否已存在该日期的考勤记录
        existing_attendance = AttendanceRepository.get_by_student_and_date(
            db, attendance_data.student_id, attendance_data.date
        )
        if existing_attendance:
            return None, "该日期的考勤记录已存在"
        
        # 创建考勤记录
        attendance = AttendanceRepository.create(db, attendance_data)
        return attendance, None
    
    @staticmethod
    def get_attendance(db: Session, attendance_id: int) -> Attendance:
        """获取考勤详情"""
        return AttendanceRepository.get_by_id(db, attendance_id)
    
    @staticmethod
    def get_attendance_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取考勤列表"""
        return AttendanceRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def update_attendance(db: Session, attendance_id: int, attendance_data: AttendanceUpdate) -> Attendance:
        """更新考勤"""
        return AttendanceRepository.update(db, attendance_id, attendance_data)
    
    @staticmethod
    def delete_attendance(db: Session, attendance_id: int) -> bool:
        """删除考勤"""
        return AttendanceRepository.delete(db, attendance_id)
