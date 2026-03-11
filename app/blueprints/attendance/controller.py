from flask import request, g
from app.blueprints.attendance import attendance_bp
from app.blueprints.attendance.service import AttendanceService
from app.blueprints.attendance.schema import AttendanceCreate, AttendanceUpdate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@attendance_bp.route('/', methods=['POST'])
@admin_required()
def create_attendance():
    """创建考勤"""
    try:
        data = request.get_json()
        attendance_data = AttendanceCreate(**data)
        attendance, msg = AttendanceService.create_attendance(db.session, attendance_data)
        if not attendance:
            return error(message=msg)
        return success(data=attendance_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@attendance_bp.route('/<int:attendance_id>', methods=['GET'])
@auth_required()
def get_attendance(attendance_id):
    """获取考勤详情"""
    try:
        attendance = AttendanceService.get_attendance(db.session, attendance_id)
        if not attendance:
            return error(message="考勤记录不存在")
        
        # 检查权限
        if not check_student_permission(attendance.student_id):
            return forbidden("权限不足")
        
        return success(data={
            "id": attendance.id,
            "student_id": attendance.student_id,
            "date": attendance.date,
            "is_present": attendance.is_present,
            "create_time": attendance.create_time,
            "update_time": attendance.update_time
        })
    except Exception as e:
        return error(message=str(e))

@attendance_bp.route('/', methods=['GET'])
@auth_required()
def get_attendance_list():
    """获取考勤列表"""
    try:
        filters = {}
        # 家长只能查看自己孩子的考勤
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
        if request.args.get('is_present') is not None:
            filters['is_present'] = int(request.args.get('is_present'))
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        
        total, items = AttendanceService.get_attendance_list(db.session, skip, limit, **filters)
        attendance_list = []
        for attendance in items:
            attendance_list.append({
                "id": attendance.id,
                "student_id": attendance.student_id,
                "date": attendance.date,
                "is_present": attendance.is_present,
                "create_time": attendance.create_time,
                "update_time": attendance.update_time
            })
        
        return success(data={"total": total, "items": attendance_list})
    except Exception as e:
        return error(message=str(e))

@attendance_bp.route('/<int:attendance_id>', methods=['PUT'])
@admin_required()
def update_attendance(attendance_id):
    """更新考勤"""
    try:
        data = request.get_json()
        attendance_data = AttendanceUpdate(**data)
        attendance = AttendanceService.update_attendance(db.session, attendance_id, attendance_data)
        if not attendance:
            return error(message="考勤记录不存在")
        return success(data={
            "id": attendance.id,
            "student_id": attendance.student_id,
            "date": attendance.date,
            "is_present": attendance.is_present,
            "create_time": attendance.create_time,
            "update_time": attendance.update_time
        }, message="更新成功")
    except Exception as e:
        return error(message=str(e))

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@admin_required()
def delete_attendance(attendance_id):
    """删除考勤"""
    try:
        success_flag = AttendanceService.delete_attendance(db.session, attendance_id)
        if not success_flag:
            return error(message="考勤记录不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))
