from flask import request, g
from app.blueprints.ai_analysis import ai_analysis_bp
from app.blueprints.ai_analysis.service import AIAnalysisService as BlueprintAIAnalysisService
from app.services.ai_analysis_service import AIAnalysisService
from app.blueprints.ai_analysis.schema import AIAnalysisCreate
from app.utils import success, error, forbidden
from app.middlewares import auth_required, admin_required, check_student_permission
from app.extensions import db

@ai_analysis_bp.route('/', methods=['POST'])
@admin_required()
def create_analysis():
    """创建AI分析"""
    try:
        data = request.get_json()
        analysis_data = AIAnalysisCreate(**data)
        analysis, msg = AIAnalysisService.create_analysis(db.session, analysis_data)
        if not analysis:
            return error(message=msg)
        return success(data=analysis_data.dict(), message="创建成功")
    except Exception as e:
        return error(message=str(e))

@ai_analysis_bp.route('/<int:analysis_id>', methods=['GET'])
@auth_required()
def get_analysis(analysis_id):
    """获取AI分析详情"""
    try:
        analysis = AIAnalysisService.get_analysis(db.session, analysis_id)
        if not analysis:
            return error(message="AI分析记录不存在")
        
        # 检查权限
        if not check_student_permission(analysis.student_id):
            return forbidden("权限不足")
        
        return success(data={
            "id": analysis.id,
            "student_id": analysis.student_id,
            "analysis_period": analysis.analysis_period,
            "analysis_content": analysis.analysis_content,
            "generate_time": analysis.generate_time,
            "create_time": analysis.create_time,
            "update_time": analysis.update_time
        })
    except Exception as e:
        return error(message=str(e))

@ai_analysis_bp.route('/', methods=['GET'])
@auth_required()
def get_analysis_list():
    """获取AI分析列表"""
    try:
        filters = {}
        # 家长只能查看自己孩子的AI分析
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
        
        # 分析周期过滤
        if request.args.get('analysis_period'):
            filters['analysis_period'] = request.args.get('analysis_period')
        
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10))
        
        total, items = AIAnalysisService.get_analysis_list(db.session, skip, limit, **filters)
        analysis_list = []
        for analysis in items:
            analysis_list.append({
                "id": analysis.id,
                "student_id": analysis.student_id,
                "analysis_period": analysis.analysis_period,
                "analysis_content": analysis.analysis_content,
                "generate_time": analysis.generate_time,
                "create_time": analysis.create_time,
                "update_time": analysis.update_time
            })
        
        return success(data={"total": total, "items": analysis_list})
    except Exception as e:
        return error(message=str(e))

@ai_analysis_bp.route('/<int:analysis_id>', methods=['DELETE'])
@admin_required()
def delete_analysis(analysis_id):
    """删除AI分析"""
    try:
        success_flag = BlueprintAIAnalysisService.delete_analysis(db.session, analysis_id)
        if not success_flag:
            return error(message="AI分析记录不存在")
        return success(message="删除成功")
    except Exception as e:
        return error(message=str(e))

@ai_analysis_bp.route('/analyze', methods=['POST'])
@admin_required()
def trigger_analysis():
    """触发AI分析"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        analysis_period = data.get('analysis_period')
        
        if not student_id or not analysis_period:
            return error(message="缺少必要参数")
        
        # 触发AI分析
        analysis, msg = AIAnalysisService.analyze_student(db.session, student_id, analysis_period)
        if not analysis:
            return error(message=msg)
        
        return success(data={
            "id": analysis.id,
            "student_id": analysis.student_id,
            "analysis_period": analysis.analysis_period,
            "analysis_content": analysis.analysis_content,
            "generate_time": analysis.generate_time,
            "create_time": analysis.create_time,
            "update_time": analysis.update_time
        }, message="分析成功")
    except Exception as e:
        return error(message=str(e))
