from flask import Blueprint, jsonify
from flask import Flask
# Create a Blueprint object
app_views = Blueprint('app_views', __name__)

from api.v1.views.states import state_bp

from api.v1.views.index import *
