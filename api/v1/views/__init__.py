#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint("/api/vi", __name__)
from api.v1.views.index import *