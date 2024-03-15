#!/usr/bin/python3
"""init Blueprint and imports index func"""

from flask import Blueprint, render_template


app_views = Blueprint('app_view', __name__)
from api.v1.views.index import *
