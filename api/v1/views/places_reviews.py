#!/usr/bin/python3
""" Place Reviews Module """

from api.v1.views import app_views
from flask import abort, Flask, jsonify, make_response
from models.place import place_amenity


@app_views.route()
