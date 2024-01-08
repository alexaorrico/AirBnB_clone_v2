from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Importing the views to register them
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.city import *
from api.v1.views.amenities import *  # Add this line
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
