#!/usr/bin/python3
""" Init file """

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.amenity import *
from api.v1.views.users import *
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
=======
from api.v1.views.amenities import *
>>>>>>> 35ab43aa11081adaf409a1af7a92bf5daabfe3ab
