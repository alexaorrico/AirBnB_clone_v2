#!/usr/bin/python3
"""__init__
"""
from flask import Blueprint

app_views = Blueprint("base", __name__, url_prefix="/api/v1")

from .index import *
from .states import *
from .cities import *
