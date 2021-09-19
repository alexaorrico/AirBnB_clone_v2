#!/usr/bin/python3
'''
create a variable app_views from app
Blueprint, url prefix is /api/v
'''


from flask import Blueprint, Flask

# APP_VIEWS
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
