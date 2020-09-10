#!/usr/bin/python3
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# disregard pep8 for this import 
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
