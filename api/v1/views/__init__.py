#!/usr/bin/python3
"""init module"""


from flask import Blueprint, render_template


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
state_views = Blueprint('states', __name__, url_prefix='/api/v1/')
city_views = Blueprint('cities', __name__, url_prefix='/api/v1/')
amenity_views = Blueprint('amenities', __name__, url_prefix='/api/v1/')
user_views = Blueprint('users', __name__, url_prefix='/api/v1/')
place_views = Blueprint('places', __name__, url_prefix='/api/v1/')
review_views = Blueprint('reviews', __name__, url_prefix='/api/v1/')
from api.v1.views.index import *
from api.v1.views.state import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
