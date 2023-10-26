#!/usr/bin/python3
"""Module contains app_views blueprint"""

from flask import Blueprint

app_views = Blueprint(
    'app_views',
    __name__,
    url_prefix='/api/v1'
)

# imported at the bottom to avoid circular import error
from api.v1.views.index import *