#!/usr/bin/python3
"""Handling CRUD for cities"""

from api.v1.views import app_views
from flask import requests, jsonify, abort
from models import storage
from models.cities import City

@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET', 'POST'])
