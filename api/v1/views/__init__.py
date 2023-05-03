#!/usr/bin/python3
'''Contains the blueprint for the API.'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''The blueprint for the AirBnB clone API.'''


from api.v1.views.index import *
