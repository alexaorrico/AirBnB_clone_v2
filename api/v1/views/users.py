#!/usr/bin/python3
"""
a new view for User objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User
