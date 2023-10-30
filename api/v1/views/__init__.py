from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views
from api.v1.views.index import *
from api.v1.views.states import *  # Import the new states view
from api.v1.views.cities import *
from api.v1.views.amenities import *
