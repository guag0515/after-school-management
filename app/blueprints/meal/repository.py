from sqlalchemy.orm import Session
from app.models import Meal
from app.blueprints.meal.schema import MealCreate, MealUpdate

class MealRepository:
    @staticmethod
    def create(db: Session, meal_data: MealCreate) -> Meal:
        """创建餐饮"""
        db_meal = Meal(
            student_id=meal_data.student_id,
            date=meal_data.date,
            breakfast=meal_data.breakfast,
            lunch=meal_data.lunch,
            dinner=meal_data.dinner
        )
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal
    
    @staticmethod
    def get_by_id(db: Session, meal_id: int) -> Meal:
        """根据ID获取餐饮"""
        return db.query(Meal).filter(Meal.id == meal_id, Meal.is_deleted == 0).first()
    
    @staticmethod
    def get_by_student_and_date(db: Session, student_id: int, date: str) -> Meal:
        """根据学生ID和日期获取餐饮"""
        return db.query(Meal).filter(
            Meal.student_id == student_id,
            Meal.date == date,
            Meal.is_deleted == 0
        ).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取餐饮列表"""
        query = db.query(Meal).filter(Meal.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('student_id'):
            query = query.filter(Meal.student_id == filters['student_id'])
        if filters.get('date_from'):
            query = query.filter(Meal.date >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Meal.date <= filters['date_to'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def update(db: Session, meal_id: int, meal_data: MealUpdate) -> Meal:
        """更新餐饮"""
        db_meal = MealRepository.get_by_id(db, meal_id)
        if db_meal:
            update_data = meal_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_meal, field, value)
            db.commit()
            db.refresh(db_meal)
        return db_meal
    
    @staticmethod
    def delete(db: Session, meal_id: int) -> bool:
        """删除餐饮（软删除）"""
        db_meal = MealRepository.get_by_id(db, meal_id)
        if db_meal:
            db_meal.is_deleted = 1
            db.commit()
            return True
        return False
