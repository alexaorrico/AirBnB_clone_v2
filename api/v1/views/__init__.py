"""
initialize the models package
"""
from flask import Blueprint


app_views = Blueprint('views', __name__)


from api.v1.views.index import *
