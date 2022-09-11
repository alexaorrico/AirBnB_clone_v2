#!/usr/bin/python3
"""register places in blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
