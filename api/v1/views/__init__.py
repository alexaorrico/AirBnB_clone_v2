#!/usr/bin/python3
'''this is the api'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''this is the blueprint'''


from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places_amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
