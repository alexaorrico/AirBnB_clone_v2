#!/usr/bin/python3
"""Init flask views"""


from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint(url_prefix='/api/v1')
