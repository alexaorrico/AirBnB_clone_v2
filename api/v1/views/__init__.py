#!/usr/bin/python3
<<<<<<< HEAD
"""create blueprint"""
=======
""" Blueprint for API """
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

<<<<<<< HEAD
if app_views is not None:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
=======
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
>>>>>>> 206a6e57f538ad1f84b5eb5219200406d63cb1c7
