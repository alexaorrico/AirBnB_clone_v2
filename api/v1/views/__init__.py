#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

import api.v1.views.cities
import api.v1.views.states
from api.v1.views.index import *
