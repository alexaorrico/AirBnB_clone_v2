#!/usr/bin/python3
<<<<<<< HEAD
"""Initialize module
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
=======
""" Blueprint for API """
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
>>>>>>> 7f463f781d2f2c16e360fbc7e590cd9adf4bcd7c
