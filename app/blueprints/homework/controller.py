from flask import request, g
from app.blueprints.homework import homework_bp
from app.blueprints.homework.service import HomeworkService
from app.blueprints.homework.schema import HomeworkCreate, HomeworkUpdate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@homework_bp.route('/', methods=['POST'])
@admin_required()
def create_homework():
    """创建作业"""
    try:
        data = request.get_json()
        homework_data = HomeworkCreate(**data)
        homework, msg = HomeworkService.create_homework(db.session, homework_data)
        if not homework:
            return error(message=msg)
        return success(data=homework_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@homework_bp.route('/<int:homework_id>', methods=['GET'])
@auth_required()
def get_homework(homework_id):
    """获取作业详情"""
    try:
        homework = HomeworkService.get_homework(db.session, homework_id)
        if not homework:
            return error(message="作业记录不存在")
        
        # 检查权限
        if not check_student_permission(homework.student_id):
            return forbidden("权限不足")
        
        return success(data={
            "id": homework.id,
            "student_id": homework.student_id,
            "date": homework.date,
            "chinese": homework.chinese,
            "math": homework.math,
            "english": homework.english,
            "science": homework.science,
            "other": homework.other,
            "completion_status": homework.completion_status,
            "teacher_evaluation": homework.teacher_evaluation,
            "create_time": homework.create_time,
            "update_time": homework.update_time
        })
    except Exception as e:
        return error(message=str(e))

@homework_bp.route('/', methods=['GET'])
@auth_required()
def get_homework_list():
    """获取作业列表"""
    try:
        filters = {}
        # 家长只能查看自己孩子的作业
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
        if request.args.get('completion_status'):
            filters['completion_status'] = request.args.get('completion_status')
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        
        total, items = HomeworkService.get_homework_list(db.session, skip, limit, **filters)
        homework_list = []
        for homework in items:
            homework_list.append({
                "id": homework.id,
                "student_id": homework.student_id,
                "date": homework.date,
                "chinese": homework.chinese,
                "math": homework.math,
                "english": homework.english,
                "science": homework.science,
                "other": homework.other,
                "completion_status": homework.completion_status,
                "teacher_evaluation": homework.teacher_evaluation,
                "create_time": homework.create_time,
                "update_time": homework.update_time
            })
        
        return success(data={"total": total, "items": homework_list})
    except Exception as e:
        return error(message=str(e))

@homework_bp.route('/<int:homework_id>', methods=['PUT'])
@admin_required()
def update_homework(homework_id):
    """更新作业"""
    try:
        data = request.get_json()
        homework_data = HomeworkUpdate(**data)
        homework = HomeworkService.update_homework(db.session, homework_id, homework_data)
        if not homework:
            return error(message="作业记录不存在")
        return success(data={
            "id": homework.id,
            "student_id": homework.student_id,
            "date": homework.date,
            "chinese": homework.chinese,
            "math": homework.math,
            "english": homework.english,
            "science": homework.science,
            "other": homework.other,
            "completion_status": homework.completion_status,
            "teacher_evaluation": homework.teacher_evaluation,
            "create_time": homework.create_time,
            "update_time": homework.update_time
        }, message="更新成功")
    except Exception as e:
        return error(message=str(e))

@homework_bp.route('/<int:homework_id>', methods=['DELETE'])
@admin_required()
def delete_homework(homework_id):
    """删除作业"""
    try:
        success_flag = HomeworkService.delete_homework(db.session, homework_id)
        if not success_flag:
            return error(message="作业记录不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))
