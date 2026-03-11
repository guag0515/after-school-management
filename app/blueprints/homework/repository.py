from sqlalchemy.orm import Session
from app.models import Homework
from app.blueprints.homework.schema import HomeworkCreate, HomeworkUpdate

class HomeworkRepository:
    @staticmethod
    def create(db: Session, homework_data: HomeworkCreate) -> Homework:
        """创建作业"""
        db_homework = Homework(
            student_id=homework_data.student_id,
            date=homework_data.date,
            chinese=homework_data.chinese,
            math=homework_data.math,
            english=homework_data.english,
            science=homework_data.science,
            other=homework_data.other,
            completion_status=homework_data.completion_status,
            teacher_evaluation=homework_data.teacher_evaluation
        )
        db.add(db_homework)
        db.commit()
        db.refresh(db_homework)
        return db_homework
    
    @staticmethod
    def get_by_id(db: Session, homework_id: int) -> Homework:
        """根据ID获取作业"""
        return db.query(Homework).filter(Homework.id == homework_id, Homework.is_deleted == 0).first()
    
    @staticmethod
    def get_by_student_and_date(db: Session, student_id: int, date: str) -> Homework:
        """根据学生ID和日期获取作业"""
        return db.query(Homework).filter(
            Homework.student_id == student_id,
            Homework.date == date,
            Homework.is_deleted == 0
        ).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取作业列表"""
        query = db.query(Homework).filter(Homework.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('student_id'):
            query = query.filter(Homework.student_id == filters['student_id'])
        if filters.get('date_from'):
            query = query.filter(Homework.date >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Homework.date <= filters['date_to'])
        if filters.get('completion_status'):
            query = query.filter(Homework.completion_status == filters['completion_status'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def update(db: Session, homework_id: int, homework_data: HomeworkUpdate) -> Homework:
        """更新作业"""
        db_homework = HomeworkRepository.get_by_id(db, homework_id)
        if db_homework:
            update_data = homework_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_homework, field, value)
            db.commit()
            db.refresh(db_homework)
        return db_homework
    
    @staticmethod
    def delete(db: Session, homework_id: int) -> bool:
        """删除作业（软删除）"""
        db_homework = HomeworkRepository.get_by_id(db, homework_id)
        if db_homework:
            db_homework.is_deleted = 1
            db.commit()
            return True
        return False
