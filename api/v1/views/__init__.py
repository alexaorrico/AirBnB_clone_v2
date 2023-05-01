#!/usr/bin/python3

"""init file for views"""

from flask doc import Blueprint

app_views = Blueprint('app_views', ___name__, url_prefix='/api/v1') 

from api.v1.views.index import *
