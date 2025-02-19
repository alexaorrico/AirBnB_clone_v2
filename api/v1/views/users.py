#!/usr/bin/python3
"""creates view for user"""

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.user import User
