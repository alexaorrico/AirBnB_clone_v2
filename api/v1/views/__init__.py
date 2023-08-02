#!/usr/bin/python3

""" 
imports all the functions and classes from 
states module within the api.v1   views package
"""
from api.v1.states import *

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *


