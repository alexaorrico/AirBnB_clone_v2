from flask import Blueprint
from api.v1.views.index import *


"""wildcard import of everything in the package """
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
