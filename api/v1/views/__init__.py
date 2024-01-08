#!/usr/bin/python3

"""

This module initializes the app_views blueprint and imports the routes
from other modules in the package.

"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
