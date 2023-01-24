#!/bin/usr/python3
""" This module contains the places_amenities view """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage

