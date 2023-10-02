#!/usr/bin/python3
"""Importation of Blueprint in flask and a module"""

from flask import Blueprint, render_template, abort
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.place_reviews import *
from api.v1.views.places import *


"""creating  a variable which is an instance of Blueprint class"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
