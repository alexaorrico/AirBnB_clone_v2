from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/views')
from api.v1.views.index import *
