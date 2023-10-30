#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

<<<<<<< HEAD
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
=======
# Import views
from api.v1.views.index import *
from api.v1.views.states import *  # Import the new states view
from api.v1.views.cities import *
from api.v1.views.amenities import *
>>>>>>> 84f4a9ee1c4103d1f3dbe18eb210bc4996364844
