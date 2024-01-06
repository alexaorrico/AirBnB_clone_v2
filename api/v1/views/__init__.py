#!/usr/bin/python3
from flask import Blueprint
from AirBnB_clone_v3.api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
