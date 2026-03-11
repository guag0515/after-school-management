from sqlalchemy.orm import Session
from app.blueprints.score.repository import ScoreRepository
from app.blueprints.score.schema import ScoreCreate, ScoreUpdate
from app.models import Score
from app.blueprints.student.repository import StudentRepository

class ScoreService:
    @staticmethod
    def create_score(db: Session, score_data: ScoreCreate) -> Score:
        """创建成绩"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, score_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 创建成绩记录
        score = ScoreRepository.create(db, score_data)
        return score, None
    
    @staticmethod
    def get_score(db: Session, score_id: int) -> Score:
        """获取成绩详情"""
        return ScoreRepository.get_by_id(db, score_id)
    
    @staticmethod
    def get_score_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取成绩列表"""
        return ScoreRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def update_score(db: Session, score_id: int, score_data: ScoreUpdate) -> Score:
        """更新成绩"""
        return ScoreRepository.update(db, score_id, score_data)
    
    @staticmethod
    def delete_score(db: Session, score_id: int) -> bool:
        """删除成绩"""
        return ScoreRepository.delete(db, score_id)
