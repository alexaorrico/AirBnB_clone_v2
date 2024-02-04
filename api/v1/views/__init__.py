from flask import Blueprint

# Create a Blueprint instance with a URL prefix of '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import the views from the index module
from api.v1.views import *
