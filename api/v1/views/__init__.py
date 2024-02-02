#!/usr/bin/python3
from flask import Blueprint

# Create Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views
from api.v1.views.index import *
from api.v1.views import states
from api.v1.views import cities
