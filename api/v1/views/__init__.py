#!/usr/bin/python3
"""
Allows transfer of NBlueprint via variable name
"""

from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('simple_page', /api/v1/views/Blueprint)
