#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.users import *
<<<<<<< HEAD
=======
from api.v1.views.places_reviews import *
>>>>>>> 03ee046fc51fc84f789bc97c4c1833891a2c707e
