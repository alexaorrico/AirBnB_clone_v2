#!/usr/bin/python3
"""Objects handle all default REStful APi actions for states"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage