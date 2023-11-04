#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, template_folder='/api/v1')

from api.v1.views.index import *
