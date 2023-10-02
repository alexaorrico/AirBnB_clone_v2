#!/usr/bin/python3
""" The init module """

from flask import Blueprint, jsonify
from flask import Flask

# Create a Blueprint object
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import api_v1_stats
app_views.register_blueprint(api_v1_stats)

from api.v1.views.states import *

