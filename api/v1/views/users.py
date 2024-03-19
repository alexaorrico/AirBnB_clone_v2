#!/usr/bin/python3
"""Users object module that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, request, current_app, abort
from models import storage
from models.user import User
