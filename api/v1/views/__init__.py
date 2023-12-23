# import flask app views modules
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *

# creates a Blueprint to execute app
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
