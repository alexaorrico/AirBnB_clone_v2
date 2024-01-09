#!/usr/bin/python3
""" Initialize views """
from flask import Flask, Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
# from api.v1.views.places import *
# from api.v1.views.places_reviews import *
# from api.v1.views.states import *
# from api.v1.views.users import *
