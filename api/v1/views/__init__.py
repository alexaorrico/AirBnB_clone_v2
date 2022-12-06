#!/usr/bin/python3
'''
Contains the blueprints for the api url builder.
'''

from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint('api', __name__, url_prefix='/api/v1')
