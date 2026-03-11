from flask import request, g
from app.blueprints.student import student_bp
from app.blueprints.student.service import StudentService, ParentService
from app.blueprints.student.schema import StudentCreate, StudentUpdate, ParentCreate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@student_bp.route('/', methods=['POST'])
@admin_required()
def create_student():
    """创建学生"""
    try:
        data = request.get_json()
        student_data = StudentCreate(**data)
        student = StudentService.create_student(db.session, student_data)
        return success(data=student_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@student_bp.route('/<int:student_id>', methods=['GET'])
@auth_required()
def get_student(student_id):
    """获取学生详情"""
    try:
        # 检查权限
        if not check_student_permission(student_id):
            return forbidden("权限不足")
        
        student = StudentService.get_student(db.session, student_id)
        if not student:
            return error(message="学生不存在")
        
        return success(data={
            "id": student.id,
            "name": student.name,
            "gender": student.gender,
            "class": student.class_,
            "service_type": student.service_type,
            "parent1_phone": student.parent1_phone,
            "parent2_phone": student.parent2_phone,
            "create_time": student.create_time,
            "update_time": student.update_time
        })
    except Exception as e:
        return error(message=str(e))

@student_bp.route('/', methods=['GET'])
@auth_required()
def get_student_list():
    """获取学生列表"""
    try:
        # 家长只能查看自己孩子的信息
        if g.user_type == 'parent':
            from app.models import Parent
            parent = Parent.query.get(g.user_id)
            if parent:
                student = StudentService.get_student(db.session, parent.student_id)
                if student:
                    return success(data={
                        "total": 1,
                        "items": [{
                            "id": student.id,
                            "name": student.name,
                            "gender": student.gender,
                            "class": student.class_,
                            "service_type": student.service_type,
                            "parent1_phone": student.parent1_phone,
                            "parent2_phone": student.parent2_phone,
                            "create_time": student.create_time,
                            "update_time": student.update_time
                        }]
                    })
                return success(data={"total": 0, "items": []})
            return success(data={"total": 0, "items": []})
        
        # 管理员可以查看所有学生
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        filters = {}
        if request.args.get('name'):
            filters['name'] = request.args.get('name')
        if request.args.get('class'):
            filters['class_'] = request.args.get('class')
        if request.args.get('service_type'):
            filters['service_type'] = request.args.get('service_type')
        
        total, items = StudentService.get_student_list(db.session, skip, limit, **filters)
        student_list = []
        for student in items:
            student_list.append({
                "id": student.id,
                "name": student.name,
                "gender": student.gender,
                "class": student.class_,
                "service_type": student.service_type,
                "parent1_phone": student.parent1_phone,
                "parent2_phone": student.parent2_phone,
                "create_time": student.create_time,
                "update_time": student.update_time
            })
        
        return success(data={"total": total, "items": student_list})
    except Exception as e:
        return error(message=str(e))

@student_bp.route('/<int:student_id>', methods=['PUT'])
@admin_required()
def update_student(student_id):
    """更新学生"""
    try:
        data = request.get_json()
        student_data = StudentUpdate(**data)
        student = StudentService.update_student(db.session, student_id, student_data)
        if not student:
            return error(message="学生不存在")
        return success(data={
            "id": student.id,
            "name": student.name,
            "gender": student.gender,
            "class": student.class_,
            "service_type": student.service_type,
            "parent1_phone": student.parent1_phone,
            "parent2_phone": student.parent2_phone,
            "create_time": student.create_time,
            "update_time": student.update_time
        }, message="更新成功")
    except Exception as e:
        return error(message=str(e))

@student_bp.route('/<int:student_id>', methods=['DELETE'])
@admin_required()
def delete_student(student_id):
    """删除学生"""
    try:
        success_flag = StudentService.delete_student(db.session, student_id)
        if not success_flag:
            return error(message="学生不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))

@student_bp.route('/parent', methods=['POST'])
@admin_required()
def create_parent():
    """创建家长"""
    try:
        data = request.get_json()
        parent_data = ParentCreate(**data)
        parent, msg = ParentService.create_parent(db.session, parent_data)
        if not parent:
            return error(message=msg)
        return success(data=parent_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))
