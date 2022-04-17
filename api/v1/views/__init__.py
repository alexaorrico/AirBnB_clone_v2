#!/usr/bin/python3
""" contains app_views blueprint """
from django import views
from flask import Blueprint

app_views = Blueprint('api', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
