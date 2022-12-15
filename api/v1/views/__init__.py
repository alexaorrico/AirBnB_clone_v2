#!/usr/bin/pythoon3
""" Create init """
from flask import Blueprint
from views.index import *

app_views = Blueprint(url_prefix='/api/v1')