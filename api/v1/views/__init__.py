#!/usr/bin/python3
<<<<<<< HEAD
""" Blueprint for API """
from flask import Blueprint
=======
""" 
Init file that turns a module into a package
"""

from flask doc import Blueprint
>>>>>>> c18aee22ec56a82b2b1c541e9134627845d1d329

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
=======
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
>>>>>>> c18aee22ec56a82b2b1c541e9134627845d1d329
from api.v1.views.places_amenities import *
