#!/usr/bin/python3
"""
    INIT BLUEPRINT AND 
    IMPORT VIEW
"""


# blueprint to import routes and state blueprints for CRUD and JSON - based
from flask import Blueprint

app_views = Blueprint('api/v1', __name__)

from api.v1.views.index import *
from api.v1.views.states import *