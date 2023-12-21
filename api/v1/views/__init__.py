from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

"""import flask app views modules"""
from api.v1.views.index import *
