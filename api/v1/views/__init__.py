from flask import Blueprint
#from api.v1.views.index import * - getting circular import error

# create an instance of Blueprint with name app_views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *


