#!/usr/bin/python3
"""Places object module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, current_app, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User
