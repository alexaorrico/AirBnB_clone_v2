from flask import Blueprint
from api.v1.views.index import *
from api.v1.views import states
from api.v1.views import cities
from api.v1.views import amenities


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
