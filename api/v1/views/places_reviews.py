#!/usr/bin/python3
"""Create view for places"""

from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City