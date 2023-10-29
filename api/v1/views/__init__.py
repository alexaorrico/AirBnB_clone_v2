#!/usr/bin/python3
"""
Blueprint for the api
"""

from api.v1.views.states import *
from api.v1.views.index import *
from flask import Blueprint, jsonify

app_views = Blueprint('app_views', __name__,
                      url_prefix=('/api/v1'))
