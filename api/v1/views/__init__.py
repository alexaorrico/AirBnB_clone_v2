#!/usr/bin/python3
""" flask stuff """
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *  # noqa: E402
from api.v1.views.states import *  # noqa: E402
from api.v1.views.cities import *  # noqa: E402
from api.v1.views.amenities import *  # noqa: E402
from api.v1.views.users import *  # noqa: E402
from api.v1.views.places import *  # noqa: E402
from api.v1.views.places_reviews import *  # noqa: E402
