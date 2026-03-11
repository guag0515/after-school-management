from sqlalchemy.orm import Session
from app.blueprints.student.repository import StudentRepository, ParentRepository
from app.blueprints.student.schema import StudentCreate, StudentUpdate, ParentCreate
from app.models import Student

class StudentService:
    @staticmethod
    def create_student(db: Session, student_data: StudentCreate) -> Student:
        """创建学生"""
        return StudentRepository.create(db, student_data)
    
    @staticmethod
    def get_student(db: Session, student_id: int) -> Student:
        """获取学生详情"""
        return StudentRepository.get_by_id(db, student_id)
    
    @staticmethod
    def get_student_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取学生列表"""
        return StudentRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def update_student(db: Session, student_id: int, student_data: StudentUpdate) -> Student:
        """更新学生"""
        return StudentRepository.update(db, student_id, student_data)
    
    @staticmethod
    def delete_student(db: Session, student_id: int) -> bool:
        """删除学生"""
        return StudentRepository.delete(db, student_id)

class ParentService:
    @staticmethod
    def create_parent(db: Session, parent_data: ParentCreate) -> Student:
        """创建家长"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, parent_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 检查手机号是否已存在
        existing_parent = ParentRepository.get_by_phone(db, parent_data.phone)
        if existing_parent:
            return None, "手机号已被注册"
        
        # 创建家长
        parent = ParentRepository.create(db, parent_data)
        return parent, None
