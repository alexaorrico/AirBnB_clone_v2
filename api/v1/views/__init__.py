#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

# Import the views after site has been defined. The views
# module will need to import 'site' so we need to make
# sure that we import views after site has been defined.
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.places import *
