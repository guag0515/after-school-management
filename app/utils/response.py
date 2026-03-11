from flask import jsonify

def success(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({
        "code": 200,
        "message": message,
        "data": data
    })

def error(code=400, message="操作失败"):
    """错误响应"""
    return jsonify({
        "code": code,
        "message": message
    }), code

def unauthorized(message="未授权访问"):
    """未授权响应"""
    return jsonify({
        "code": 401,
        "message": message
    }), 401

def forbidden(message="权限不足"):
    """权限不足响应"""
    return jsonify({
        "code": 403,
        "message": message
    }), 403
