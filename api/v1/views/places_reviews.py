#!/usr/bin/python3
"""Reviews object module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, current_app, abort
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
