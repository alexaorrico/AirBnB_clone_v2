#!/usr/bin/python3
"""View for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
