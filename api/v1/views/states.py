#!/usr/bin/python3
""" Handles all State requests for the API """

from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def all(states):
    """ Returns a JSON of State objects """
    
