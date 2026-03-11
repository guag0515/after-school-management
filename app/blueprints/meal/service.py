from sqlalchemy.orm import Session
from app.blueprints.meal.repository import MealRepository
from app.blueprints.meal.schema import MealCreate, MealUpdate
from app.models import Meal
from app.blueprints.student.repository import StudentRepository

class MealService:
    @staticmethod
    def create_meal(db: Session, meal_data: MealCreate) -> Meal:
        """创建餐饮"""
        # 检查学生是否存在
        student = StudentRepository.get_by_id(db, meal_data.student_id)
        if not student:
            return None, "学生不存在"
        
        # 检查是否已存在该日期的餐饮记录
        existing_meal = MealRepository.get_by_student_and_date(
            db, meal_data.student_id, meal_data.date
        )
        if existing_meal:
            return None, "该日期的餐饮记录已存在"
        
        # 创建餐饮记录
        meal = MealRepository.create(db, meal_data)
        return meal, None
    
    @staticmethod
    def get_meal(db: Session, meal_id: int) -> Meal:
        """获取餐饮详情"""
        return MealRepository.get_by_id(db, meal_id)
    
    @staticmethod
    def get_meal_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取餐饮列表"""
        return MealRepository.get_list(db, skip, limit, **filters)
    
    @staticmethod
    def update_meal(db: Session, meal_id: int, meal_data: MealUpdate) -> Meal:
        """更新餐饮"""
        return MealRepository.update(db, meal_id, meal_data)
    
    @staticmethod
    def delete_meal(db: Session, meal_id: int) -> bool:
        """删除餐饮"""
        return MealRepository.delete(db, meal_id)
