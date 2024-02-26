
from flask import Blueprint
app_views = Blueprint('app-views', __name__, url_prefix='/api/v1/')

from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.index import *
