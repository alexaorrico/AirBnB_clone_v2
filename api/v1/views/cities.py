#!/usr/bin/python3
"""Create view for cities"""

from flask import Flask, jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State

