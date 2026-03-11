from sqlalchemy.orm import Session
from app.models import AIAnalysis
from app.blueprints.ai_analysis.schema import AIAnalysisCreate

class AIAnalysisRepository:
    @staticmethod
    def create(db: Session, analysis_data: AIAnalysisCreate) -> AIAnalysis:
        """创建AI分析"""
        db_analysis = AIAnalysis(
            student_id=analysis_data.student_id,
            analysis_period=analysis_data.analysis_period,
            analysis_content=analysis_data.analysis_content
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        return db_analysis
    
    @staticmethod
    def get_by_id(db: Session, analysis_id: int) -> AIAnalysis:
        """根据ID获取AI分析"""
        return db.query(AIAnalysis).filter(AIAnalysis.id == analysis_id, AIAnalysis.is_deleted == 0).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取AI分析列表"""
        query = db.query(AIAnalysis).filter(AIAnalysis.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('student_id'):
            query = query.filter(AIAnalysis.student_id == filters['student_id'])
        if filters.get('analysis_period'):
            query = query.filter(AIAnalysis.analysis_period == filters['analysis_period'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def delete(db: Session, analysis_id: int) -> bool:
        """删除AI分析（软删除）"""
        db_analysis = AIAnalysisRepository.get_by_id(db, analysis_id)
        if db_analysis:
            db_analysis.is_deleted = 1
            db.commit()
            return True
        return False
