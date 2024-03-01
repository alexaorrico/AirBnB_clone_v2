#!/usr/bin/python3
""" New City view """

from api.v1.views import app_views
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities')
