#!/usr/bin/python3
"""Importing Blueprint"""

from flask import Blueprint

# Creates an instance Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/vi")

from api.vi.views.index import *
from api.vi.views.states import *
from api.vi.views.cities import *
from api.vi.views.amenities import *
from api.vi.views.places import *
from api.vi.views.users import *
from api.vi.views.places_reviews import *