from flask import Blueprint

score_bp = Blueprint('score', __name__)

from app.blueprints.score import controller
