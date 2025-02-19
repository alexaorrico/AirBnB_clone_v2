#!/usr/bin/python3
"""Blueprint setup for the API"""


from flask import Blueprint


# Create a new Blueprint for API routes with a URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Import view modules if the blueprint is successfully created
if app_views is not None:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
