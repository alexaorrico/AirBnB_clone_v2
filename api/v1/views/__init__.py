#!/usr/bin/python3
"""Creating Blueprint views"""

from flask import Blueprint
from models.state import State
from api.v1.views.states import *

app_views = Blueprint('app_view', __name__, url_prefix='/api/v1')
