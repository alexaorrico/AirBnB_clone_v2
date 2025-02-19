# api/v1/views/blueprint.py
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
