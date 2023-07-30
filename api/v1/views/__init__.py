from flask import Blueprint

# Create the Blueprint object with '/api/v1' as url_prefix

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *


