#!/usr/bin/python3
# init file to import app_views blueprint
from flask import Blueprint


app_views = Blueprint('status', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
