#!/usr/bin/python3
""" Initialize the views package """

from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint()
