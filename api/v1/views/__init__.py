#!/usr/bin/python3
"""views root file for describing blueprints"""

from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

import api.v1.views.index
import api.v1.views.states
