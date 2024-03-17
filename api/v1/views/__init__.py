#!/usr/bin/python3
""" Set up Flask blueprint """
from flask import Blueprint


# Create blueprint instance and set url prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Wildcard import to prevent circular import
from api.v1.views.index import *

# Import States
from api.v1.views.states import *

# Import Cities.
from api.v1.views.cities import *

#Import Amenities
from api.v1.views.amenities import *

#Import Users
from api.v1.views.users import *

#Import Places
from api.v1.views.places import *

#Import Reviews
from api.v1.views.places_reviews import *
