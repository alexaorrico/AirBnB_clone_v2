#!/usr/bin/python3
""" This code initializes a Flask Blueprint """

from flask import Blueprint
from api.v1.views import index

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
