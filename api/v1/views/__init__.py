#!/usr/bin/python3
"""
This module declares the blueprint of the system
"""
from flask import Blueprint
from .cities import get_all_cities, get_city, create_city, delete_city, update_city


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *


app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'])(get_all_cities)
app_views.route('/api/v1/cities/<city_id>', methods=['GET'])(get_city)
app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'])(delete_city)
app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'])(create_city)
app_views.route('/api/v1/cities/<city_id>', methods=['PUT'])(update_city)
