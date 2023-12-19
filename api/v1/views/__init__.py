from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# PEP8 will complain about this wildcard import, but it's necessary to avoid circular import errors
