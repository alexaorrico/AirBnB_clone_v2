#!/usr/bin/python3
"""
Creates a Blueprint instance with the url_prefix set /api/vi
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.vi.views.index import *
from api.vi.views.states import *
from api.vi.views.cities import *
from api.vi.views.amenities import *
from api.vi.views.users import *
from api.vi.views.places import *
from api.vi.views.places_reviews import *
from api.vi.views.places_amenities import *