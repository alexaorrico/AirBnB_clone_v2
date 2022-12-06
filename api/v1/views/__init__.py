from flask import Blueprint
app_viwes = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
