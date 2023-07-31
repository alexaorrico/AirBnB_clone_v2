#!/usr/bin/python3
"""Creating Blueprint views"""

from flask import Blueprint
# from api.v1.views import *

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')
