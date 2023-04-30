#!/usr/bin/python3
"""Init the package
Note: importing line 10 after line 6
raises an error: Circular import"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
