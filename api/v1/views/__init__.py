#!/usr/bin/python3
""" Blue print for the API """
from flask import Blueprint


app_views = Blueprint('app_views',__name__, url_prefix='/api/v1')
""" Blueprint for API """

from api.v1.views.index import *
