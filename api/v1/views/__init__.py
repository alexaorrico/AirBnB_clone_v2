#!/usr/bin/python3
""" Blue print for the API """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
state_view = Blueprint('state_view', __name__, url_prefix='/api/v1')
place_view = Blueprint('place_view', __name__, url_prefix='/api/v1')
reviews_view = Blueprint('reviews_view', __name__, url_prefix='/api/v1')
""" Blueprint for API """

from api.v1.views.index import *
from api.v1.views.states import state_view
from api.v1.views.places import place_view
from api.v1.views.places_reviews import reviews_view
