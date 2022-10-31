#!/usr/bin/python3
"""
view Blueprint
"""


from flask import Blueprint

# import views after the site has been defined
from api.v1.views.index import *

from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.states import *
from api.v1.views.places_reviews import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
