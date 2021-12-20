#!/usr/bin/python3
''' Intialiaze  views module'''


from api.v1.views.places_reviews import *  # will not be checked
from api.v1.views.places import *  # will not be checked
from api.v1.views.users import *  # will not be checked
from api.v1.views.amenities import *  # will not be checked
from api.v1.views.cities import *  # will not be checked
from api.v1.views.states import *  # will not be checked
from api.v1.views.index import *  # will not be checked
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
