#!/usr/bin/pyhton3
"""import blueprint"""

from flask import Blueprint

app_views = Blueprint('status', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
