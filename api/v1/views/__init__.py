#!/usr/bin/python3
"""This is a blueprint for my APIs"""
from  flask import Blueprint
import * from api.v1.views.index

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
