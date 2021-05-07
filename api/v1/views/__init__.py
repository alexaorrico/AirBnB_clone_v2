#!/usr/bin/python3
'''Create app_views and initialize views folder'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *