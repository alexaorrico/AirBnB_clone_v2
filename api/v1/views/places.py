#!/usr/bin/python3
"""place view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place