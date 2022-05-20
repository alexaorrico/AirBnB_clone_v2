#!/usr/bin/python3
"""
This is an init module that define define a blueprint
"""
from flask import Blueprint

app_views = Blueprint('api',__name__,url_prefix='/api/v1')

from api.v1.views.index import *
