#!/usr/bin/python3
"""The host file for api blueprint."""

# Importing modules from system files
from flask import Blueprint


# The blueprint for API of AirBnB clone
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing modules from AirBnB Clone project files
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *

# Importing views for Amenity
from api.v1.views.amenities import *

# Importng views for User
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
