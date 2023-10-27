#!/usr/bin/python3
"""Initializes views by creating a flask blueprint"""
from flask import Blueprint

app_views = Blueprint('restful_api', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
