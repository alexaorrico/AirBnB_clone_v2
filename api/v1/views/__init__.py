from flask import Blueprint

app_views = Blueprint('app-views', __name__, url_prefix='/api/v1/')

from api.v1.views.index import *
from api.vi.views.states import *
from api.vi.views.cities import *
