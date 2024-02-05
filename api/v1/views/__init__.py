from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('views', __name__)
