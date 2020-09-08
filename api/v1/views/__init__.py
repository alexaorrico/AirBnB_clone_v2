#!/usr/bin/python3
    """[Blueprint and wildcard import of everything]
    """

from flask doc import Blueprint
app_views = Blueprint('app', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
