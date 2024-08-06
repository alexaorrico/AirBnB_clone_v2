from api.v1.views import places_reviews
from api.v1.views import users
from api.v1.views import amenities
from api.v1.views import cities
from api.v1.views import states
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__,  url_prefix='/api/v1')
