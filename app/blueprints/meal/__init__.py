from flask import Blueprint

meal_bp = Blueprint('meal', __name__)

from app.blueprints.meal import controller
