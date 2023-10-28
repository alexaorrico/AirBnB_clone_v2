#!/usr/bin/python3
"""The host file for api blueprint."""

# Importing modules from system files
from flask import Blueprint

# Importing modules from my files
from api.v1.views.index import *


# The blueprint for API of AirBnB clone
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
