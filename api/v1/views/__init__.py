from flask import Blueprint


# Create a Blueprint instance with a prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
