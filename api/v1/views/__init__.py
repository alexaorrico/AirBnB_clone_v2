#!/usr/bin/python3
'''Blueprint for the API'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
''' Blueprint for Airbnb clone API'''

from api.v1.views.index import *
