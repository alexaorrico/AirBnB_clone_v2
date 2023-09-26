from flask import Blueprint

# Create a Blueprint instance with URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import from 'index' module within 'views'
from . import index