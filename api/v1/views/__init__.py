#!/usr/bin/python3

"""init file for views module"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
