from flask import Blueprint


"""
create a blueprint instance
"""

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views modules
from api.v1.views.index import *
