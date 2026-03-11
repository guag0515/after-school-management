from sqlalchemy.orm import Session
from app.models import Score
from app.blueprints.score.schema import ScoreCreate, ScoreUpdate

class ScoreRepository:
    @staticmethod
    def create(db: Session, score_data: ScoreCreate) -> Score:
        """创建成绩"""
        db_score = Score(
            student_id=score_data.student_id,
            subject=score_data.subject,
            exam_type=score_data.exam_type,
            score=score_data.score,
            exam_time=score_data.exam_time
        )
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
        return db_score
    
    @staticmethod
    def get_by_id(db: Session, score_id: int) -> Score:
        """根据ID获取成绩"""
        return db.query(Score).filter(Score.id == score_id, Score.is_deleted == 0).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取成绩列表"""
        query = db.query(Score).filter(Score.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('student_id'):
            query = query.filter(Score.student_id == filters['student_id'])
        if filters.get('subject'):
            query = query.filter(Score.subject == filters['subject'])
        if filters.get('exam_type'):
            query = query.filter(Score.exam_type == filters['exam_type'])
        if filters.get('exam_time_from'):
            query = query.filter(Score.exam_time >= filters['exam_time_from'])
        if filters.get('exam_time_to'):
            query = query.filter(Score.exam_time <= filters['exam_time_to'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def update(db: Session, score_id: int, score_data: ScoreUpdate) -> Score:
        """更新成绩"""
        db_score = ScoreRepository.get_by_id(db, score_id)
        if db_score:
            update_data = score_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_score, field, value)
            db.commit()
            db.refresh(db_score)
        return db_score
    
    @staticmethod
    def delete(db: Session, score_id: int) -> bool:
        """删除成绩（软删除）"""
        db_score = ScoreRepository.get_by_id(db, score_id)
        if db_score:
            db_score.is_deleted = 1
            db.commit()
            return True
        return False
