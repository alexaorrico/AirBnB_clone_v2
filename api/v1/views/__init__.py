#!/usr/bin/python3
""" Importing, creating variables, dealing with wildcards """
from flask import Blueprint


app_views = Blueprint('app_views', __name__)

from api.v1.views.index import *
