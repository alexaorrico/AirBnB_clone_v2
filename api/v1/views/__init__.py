#!/usr/bin/python3
"""Creates blueprint with url prefix /api/v4 """
from flask import Blueprint
<<<<<<< HEAD
=======
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
>>>>>>> 19d1d85b0daacbd7ea743005ecc4152d60a5e794
from api.v1.views.places_amenities import *
from api.v1.views.places_reviews import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
