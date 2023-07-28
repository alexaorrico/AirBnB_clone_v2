#!/usr/bin/python3
"""
import Blueprint from flask doc
create a variable app_views which is an instance of 
Blueprint (url prefix must be /api/v1)
wildcard import of everything in the package api.v1.views.index
"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint("/api/v1", __name__)
