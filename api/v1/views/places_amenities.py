#!/usr/bin/python3
"""new view for Place and amenities object that handles all default"""

from api.v1.views import app_views
from models import storage
from flask import Flask, abort, jsonify, make_response
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User
from flask import request
from models.state import State

