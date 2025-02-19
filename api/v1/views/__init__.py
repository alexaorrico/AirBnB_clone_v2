#!/usr/bin/python3
"""Blueprint Module"""


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *  # importing the index view
from api.v1.views.states import *  # importing the states view
from api.v1.views.cities import *  # importing the cities view
from api.v1.views.amenities import *  # importing the amenities view 
from api.v1.views.users import *  # importing the the users view
from api.v1.views.places import *  # importing the places view
from api.v1.views.places_reviews import *  # importing the places_reviews view
