#!/usr/bin/python3
""" Blueprint for API v1 """
from flask import Blueprint, abort, request
import index
import users
import states
import cities
import amenities
import places
import places_reviews

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
__all__ = ['index',
           'user',
           'states',
           'cities',
           'amenities',
           'places',
           'places_reviews'
           ]
