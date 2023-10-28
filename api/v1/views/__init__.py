#!/usr/bin/python3
"""
initialize the models package
"""

from flask import Blueprint, jsonify
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__,
                        url_prefix=('/api/v1'))
