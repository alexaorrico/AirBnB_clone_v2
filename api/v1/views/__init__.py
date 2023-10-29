#!/usr/bin/python3
"""
this module initializes the blueprints
that are associated with the api
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if app_views:
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.cities import *
<<<<<<< HEAD
    from api.v1.views.ameities import *
    from api.v1.views.users import *
=======
    from api.v1.views.amenities import *
>>>>>>> 97e69c3d4d10ad114ac929dad78ca8163a0e258c
