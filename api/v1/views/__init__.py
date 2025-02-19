#!/usr/bin/python3
"""Creating Flask blueprint App_views"""

from api.v1.views.index import *
from flask import Flask, Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='api/v1')
