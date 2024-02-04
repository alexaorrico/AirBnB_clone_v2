#!/usr/bin/python3
"""amenities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
