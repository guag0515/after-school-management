from sqlalchemy.orm import Session
from app.blueprints.ai_analysis.repository import AIAnalysisRepository
from app.blueprints.ai_analysis.schema import AIAnalysisCreate
from app.models import AIAnalysis
from app.blueprints.student.repository import StudentRepository

class AIAnalysisService:
    @staticmethod
    def create_analysis(db: Session, analysis_data: AIAnalysisCreate) -> AIAnalysis:
        """创建AI分析"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, analysis_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 创建AI分析记录
        analysis = AIAnalysisRepository.create(db, analysis_data)
        return analysis, None
    
    @staticmethod
    def get_analysis(db: Session, analysis_id: int) -> AIAnalysis:
        """获取AI分析详情"""
        return AIAnalysisRepository.get_by_id(db, analysis_id)
    
    @staticmethod
    def get_analysis_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取AI分析列表"""
        return AIAnalysisRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def delete_analysis(db: Session, analysis_id: int) -> bool:
        """删除AI分析"""
        return AIAnalysisRepository.delete(db, analysis_id)
