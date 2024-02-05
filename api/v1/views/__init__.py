#!/usr/bin/python3
'''Initialize Flask Blueprint for API views.'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''Blueprint clone API.'''


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
