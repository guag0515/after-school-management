from app.blueprints.admin import admin_bp
from flask import jsonify

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """管理员仪表盘"""
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'dashboard': 'Admin Dashboard'
        }
    })
