#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint('status', __name__, url_prefix='/api/va')
#import api.v1.views.index
