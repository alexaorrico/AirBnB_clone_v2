#!/usr/bin/python3

"""View module"""

from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint("/api/v1")
