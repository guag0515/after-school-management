from flask import request, g
from app.blueprints.score import score_bp
from app.blueprints.score.service import ScoreService
from app.blueprints.score.schema import ScoreCreate, ScoreUpdate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@score_bp.route('/', methods=['POST'])
@admin_required()
def create_score():
    """创建成绩"""
    try:
        data = request.get_json()
        score_data = ScoreCreate(**data)
        score, msg = ScoreService.create_score(db.session, score_data)
        if not score:
            return error(message=msg)
        return success(data=score_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@score_bp.route('/<int:score_id>', methods=['GET'])
@auth_required()
def get_score(score_id):
    """获取成绩详情"""
    try:
        score = ScoreService.get_score(db.session, score_id)
        if not score:
            return error(message="成绩记录不存在")
        
        # 检查权限
        if not check_student_permission(score.student_id):
            return forbidden("权限不足")
        
        return success(data={
            "id": score.id,
            "student_id": score.student_id,
            "subject": score.subject,
            "exam_type": score.exam_type,
            "score": float(score.score),
            "exam_time": score.exam_time,
            "create_time": score.create_time,
            "update_time": score.update_time
        })
    except Exception as e:
        return error(message=str(e))

@score_bp.route('/', methods=['GET'])
@auth_required()
def get_score_list():
    """获取成绩列表"""
    try:
        filters = {}
        # 家长只能查看自己孩子的成绩
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
        
        # 其他过滤条件
        if request.args.get('subject'):
            filters['subject'] = request.args.get('subject')
        if request.args.get('exam_type'):
            filters['exam_type'] = request.args.get('exam_type')
        if request.args.get('exam_time_from'):
            filters['exam_time_from'] = request.args.get('exam_time_from')
        if request.args.get('exam_time_to'):
            filters['exam_time_to'] = request.args.get('exam_time_to')
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        
        total, items = ScoreService.get_score_list(db.session, skip, limit, **filters)
        score_list = []
        for score in items:
            score_list.append({
                "id": score.id,
                "student_id": score.student_id,
                "subject": score.subject,
                "exam_type": score.exam_type,
                "score": float(score.score),
                "exam_time": score.exam_time,
                "create_time": score.create_time,
                "update_time": score.update_time
            })
        
        return success(data={"total": total, "items": score_list})
    except Exception as e:
        return error(message=str(e))

@score_bp.route('/<int:score_id>', methods=['PUT'])
@admin_required()
def update_score(score_id):
    """更新成绩"""
    try:
        data = request.get_json()
        score_data = ScoreUpdate(**data)
        score = ScoreService.update_score(db.session, score_id, score_data)
        if not score:
            return error(message="成绩记录不存在")
        return success(data={
            "id": score.id,
            "student_id": score.student_id,
            "subject": score.subject,
            "exam_type": score.exam_type,
            "score": float(score.score),
            "exam_time": score.exam_time,
            "create_time": score.create_time,
            "update_time": score.update_time
        }, message="更新成功")
    except Exception as e:
        return error(message=str(e))

@score_bp.route('/<int:score_id>', methods=['DELETE'])
@admin_required()
def delete_score(score_id):
    """删除成绩"""
    try:
        success_flag = ScoreService.delete_score(db.session, score_id)
        if not success_flag:
            return error(message="成绩记录不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))
