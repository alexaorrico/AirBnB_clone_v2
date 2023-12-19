from api.v1.views.index import *
from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
