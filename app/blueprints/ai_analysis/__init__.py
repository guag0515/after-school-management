from flask import Blueprint

ai_analysis_bp = Blueprint('ai_analysis', __name__)

from app.blueprints.ai_analysis import controller
