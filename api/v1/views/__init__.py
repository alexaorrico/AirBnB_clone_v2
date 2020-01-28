from flask import Blueprint
app_views = Blueprint("/api/v1")
from api.v1.views.index import *
