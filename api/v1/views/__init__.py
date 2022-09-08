from flask import Blueprint
import api.v1.views.index

app_views = Blueprint('api', __name__, url_prefix='/api/v1')
