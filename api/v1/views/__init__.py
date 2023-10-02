#!/usr/bin/python3
"""
set up a view Blueprint
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from .index import *
from .cities import *
