from sqlalchemy.orm import Session
from app.blueprints.homework.repository import HomeworkRepository
from app.blueprints.homework.schema import HomeworkCreate, HomeworkUpdate
from app.models import Homework
from app.blueprints.student.repository import StudentRepository

class HomeworkService:
    @staticmethod
    def create_homework(db: Session, homework_data: HomeworkCreate) -> Homework:
        """创建作业"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, homework_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 检查是否已存在该日期的作业记录
        existing_homework = HomeworkRepository.get_by_student_and_date(
            db, homework_data.student_id, homework_data.date
        )
        if existing_homework:
            return None, "该日期的作业记录已存在"
        
        # 创建作业记录
        homework = HomeworkRepository.create(db, homework_data)
        return homework, None
    
    @staticmethod
    def get_homework(db: Session, homework_id: int) -> Homework:
        """获取作业详情"""
        return HomeworkRepository.get_by_id(db, homework_id)
    
    @staticmethod
    def get_homework_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取作业列表"""
        return HomeworkRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def update_homework(db: Session, homework_id: int, homework_data: HomeworkUpdate) -> Homework:
        """更新作业"""
        return HomeworkRepository.update(db, homework_id, homework_data)
    
    @staticmethod
    def delete_homework(db: Session, homework_id: int) -> bool:
        """删除作业"""
        return HomeworkRepository.delete(db, homework_id)
