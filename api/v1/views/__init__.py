from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from .cities import *
from .amenities import *
from .users import *
from .places import *
from .places_reviews import *
from .places_amenities import *
