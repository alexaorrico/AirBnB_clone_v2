#!/usr/bin/python3
"""
Import [Blueprint] from [flask doc]
creatae a variable [app_views] which is an instance of [Blueprint] (url prefix m ust be [/api/v1)
wildcard import os everything in the package [api.v1.views.index] 
"""

from flask import Blueprint

app_views = Blueprint('app_views' , __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
