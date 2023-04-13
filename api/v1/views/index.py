#!/usr/bin/python3
"""
api status page Blueprint module
containing the API's status being ok or not
and the amount of objs of each type in
'storage.all'

For more information, look a <root>/models/.
"""
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from flask import jsonify


@app_views.route("/status")
def check_status():
    """ return status ok as json"""
    dict_ = {'status': "OK"}

    return jsonify(dict_)


@app_views.route('/stats')
def model_statistics():
    """
    Returns the counts of all the
    objects in 'storage.all()',
    counted by each type
    """
    return {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
