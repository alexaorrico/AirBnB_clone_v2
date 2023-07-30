#!/usr/bin/python3
"""
Handle apis from users
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
