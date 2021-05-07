#!/usr/bin/python3
""" cities """

import flask
from models import storage
from models.city import City
from api.v1.views import app_views

def all_city():
    """
    Retrieves the list of all city objects
    """
    
