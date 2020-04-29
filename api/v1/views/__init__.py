#!/usr/bin/python3
""" import files and blueprint """
from flask import Blueprint

app_views = Blueprint('status', __name__, url_prefix='/api/v1')

from api.v1.views import index
from api.v1.views.states import *
from api.v1.views.amenities import *
