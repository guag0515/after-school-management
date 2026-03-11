from flask import request, g
from app.blueprints.meal import meal_bp
from app.blueprints.meal.service import MealService
from app.blueprints.meal.schema import MealCreate, MealUpdate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@meal_bp.route('/', methods=['POST'])
@admin_required()
def create_meal():
    """创建餐饮"""
    try:
        data = request.get_json()
        meal_data = MealCreate(**data)
        meal, msg = MealService.create_meal(db.session, meal_data)
        if not meal:
            return error(message=msg)
        return success(data=meal_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@meal_bp.route('/<int:meal_id>', methods=['GET'])
@auth_required()
def get_meal(meal_id):
    """获取餐饮详情"""
    try:
        meal = MealService.get_meal(db.session, meal_id)
        if not meal:
            return error(message="餐饮记录不存在")
        
        # 检查权限
        if not check_student_permission(meal.student_id):
            return forbidden("权限不足")
        
        return success(data={
            "id": meal.id,
            "student_id": meal.student_id,
            "date": meal.date,
            "breakfast": meal.breakfast,
            "lunch": meal.lunch,
            "dinner": meal.dinner,
            "create_time": meal.create_time,
            "update_time": meal.update_time
        })
    except Exception as e:
        return error(message=str(e))

@meal_bp.route('/', methods=['GET'])
@auth_required()
def get_meal_list():
    """获取餐饮列表"""
    try:
        filters = {}
        # 家长只能查看自己孩子的餐饮
        if g.user_type == 'parent':
            from app.models import Parent
            parent = Parent.query.get(g.user_id)
            if parent:
                filters['student_id'] = parent.student_id
            else:
                return success(data={"total": 0, "items": []})
        elif g.user_type == 'admin':
            # 管理员可以指定学生ID
            if request.args.get('student_id'):
                filters['student_id'] = int(request.args.get('student_id'))
        
        # 日期范围过滤
        if request.args.get('date_from'):
            filters['date_from'] = request.args.get('date_from')
        if request.args.get('date_to'):
            filters['date_to'] = request.args.get('date_to')
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        
        total, items = MealService.get_meal_list(db.session, skip, limit, **filters)
        meal_list = []
        for meal in items:
            meal_list.append({
                "id": meal.id,
                "student_id": meal.student_id,
                "date": meal.date,
                "breakfast": meal.breakfast,
                "lunch": meal.lunch,
                "dinner": meal.dinner,
                "create_time": meal.create_time,
                "update_time": meal.update_time
            })
        
        return success(data={"total": total, "items": meal_list})
    except Exception as e:
        return error(message=str(e))

@meal_bp.route('/<int:meal_id>', methods=['PUT'])
@admin_required()
def update_meal(meal_id):
    """更新餐饮"""
    try:
        data = request.get_json()
        meal_data = MealUpdate(**data)
        meal = MealService.update_meal(db.session, meal_id, meal_data)
        if not meal:
            return error(message="餐饮记录不存在")
        return success(data={
            "id": meal.id,
            "student_id": meal.student_id,
            "date": meal.date,
            "breakfast": meal.breakfast,
            "lunch": meal.lunch,
            "dinner": meal.dinner,
            "create_time": meal.create_time,
            "update_time": meal.update_time
        }, message="更新成功")
    except Exception as e:
        return error(message=str(e))

@meal_bp.route('/<int:meal_id>', methods=['DELETE'])
@admin_required()
def delete_meal(meal_id):
    """删除餐饮"""
    try:
        success_flag = MealService.delete_meal(db.session, meal_id)
        if not success_flag:
            return error(message="餐饮记录不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))
