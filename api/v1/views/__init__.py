#!/usr/bin/python3
"""
blueprint
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.states import *
=======
#from api.v1.views.states import *
from api.v1.views.cities import *
>>>>>>> 243c48b470bf5461b394c3a4afafba2dff00be12
