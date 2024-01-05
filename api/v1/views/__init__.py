#!/usr/bin/python3
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('/api/v1', __name__, template_folder='templates')
