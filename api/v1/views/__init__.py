"""Module that creates the blueprint of app_views"""
from api.v1.views.index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
