# api/v1/views/__init__.py
"""Init file for views module"""
from flask import Blueprint
import sys

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

sys.path.append('/AirBnB_clone_v3/api/vi/views')

from index import *  
from states import *  
from cities import *  
from amenities import *
from users import *  
from places import * 
from places_reviews import * 
from places_amenities import * 
