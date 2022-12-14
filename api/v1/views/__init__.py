#!/usr/bin/python3
"""blueprint init"""

from flask import Blueprint
from views.index import *


app_views = Blueprint(url_prefix='/api/v1')
