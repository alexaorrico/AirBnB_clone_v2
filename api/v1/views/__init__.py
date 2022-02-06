#!/usr/bin/python3
""" __init__ package """


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
import api.v1.views.states
import api.v1.views.cities
import api.v1.views.amenities
import api.v1.views.users
