#!/usr/bin/python3
"""Blueprint for API"""

from api.v1.views.index import index
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

app_views.add_url_rule('/index', view_func=index,
                       methods=['GET'], strict_slashes=False)
app_views.register_blueprint(state_blueprint)
