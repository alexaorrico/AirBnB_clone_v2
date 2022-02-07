from flask import Blueprint
"""
Blueprints module to register operaions
on an application
"""

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
import api.v1.views.states
import api.v1.views.cities
import api.v1.views.amenities
import api.v1.views.users
import api.v1.views.places
import api.v1.views.places_reviews
