"""Initializes main blueprint for flask application"""
from flask import Blueprint

app_views = Blueprint("site", __name__)
from api.v1.views.index import *  # 
from api.v1.views.states import *  # n
from api.v1.views.cities import *  # 
from api.v1.views.amenities import *  n
from api.v1.views.users import *  
from api.v1.views.places import *  # 
from api.v1.views.places_reviews import *  # 
from api.v1.views.places_amenities import *  #
