# api/v1/views/__init__.py
"""Init file for views module"""
from flask import Blueprint
import sys

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

sys.path.append('/AirBnB_clone_v3/api/vi')

from views.index import *  
from views.states import *  
from views.cities import *  
from views.amenities import *
from views.users import *  
from views.places import * 
from views.places_reviews import * 
from views.places_amenities import * 
