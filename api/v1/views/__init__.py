from flask import Blueprint, jsonify
from api.v1.views.index import *
# Create a Blueprint object
app_views = Blueprint('app_views', __name__)
