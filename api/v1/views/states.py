#!/usr/bin/python3
""" New view for states object that handles all
default RESTFul API actions. """

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State

app_views.route('/states', methods=['GET'], strict_slashes=False)
def fetch_states():
  """ Retrieves the list of all State objects. """
  objs = storage.all(State).values()
  list_objs = []
  
  for obj in objs:
    list_objs.append(obj.to_dict())


