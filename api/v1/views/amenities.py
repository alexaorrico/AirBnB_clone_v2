#!/usr/bin/python3
"""ammonite colony"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity

