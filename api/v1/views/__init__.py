#!/usr/bin/python3
<<<<<<< HEAD
'''
Creates Blueprint instance with `url_prefix` set `/api/v1`.
'''


=======
"""create blueprint"""
>>>>>>> 6a3b9b65fb88b26a94fce1815dc7223dece11944
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

<<<<<<< HEAD
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
=======
if app_views is not None:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
    from api.v1.views.amenities import *
    from api.v1.views.users import *
    from api.v1.views.places import *
    from api.v1.views.places_reviews import *
    from api.v1.views.places_amenities import *
>>>>>>> 6a3b9b65fb88b26a94fce1815dc7223dece11944
