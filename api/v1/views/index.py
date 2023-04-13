#!/usr/bin/python3
<<<<<<< HEAD
import json

from flask import jsonify

from api.v1.views import app_views

=======
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

>>>>>>> 72c2052882cf43eedee79d8e5c351fe895479708

@app_views.route("/status")
def check_status():
    """ return status ok as json"""
    dict_ = { 'status' : "OK"}
    
    return jsonify(dict_)


@app_views.route('/api/v1/stats')
def model_statistics():
    """
    Returns the counts of all the
    objects in 'storage.all()',
    counted by each type
    """
    return {
        obj_type: storage.count(obj_type)
        for obj_type in (
            BaseModel,
            User,
            State,
            City,
            Amenity,
            Place,
            Review
        )
    }
