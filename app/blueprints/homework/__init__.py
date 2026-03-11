from flask import Blueprint

homework_bp = Blueprint('homework', __name__)

from app.blueprints.homework import controller
