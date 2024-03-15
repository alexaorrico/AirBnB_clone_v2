from flask import Blueprint, render_template


app_views = Blueprint('app_view', __name__)
from api.v1.views.index import *

