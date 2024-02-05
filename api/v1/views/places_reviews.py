#!/usr/bin/python3
"""This module contains the view for the place resource."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


