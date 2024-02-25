#!/usr/bin/python3
'''__init__.py file'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
