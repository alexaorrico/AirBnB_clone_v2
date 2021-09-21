#!/usr/bin/python3
""" built api """
from api.vi.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models import storage
from models.user import User

@app_views.route('\status')
def json_return():
    return jsonfy({'status': "OK"})

@app_views.route('\stats')
def return_num_objects():
    classes = {"amenities": Amenity, "cities": City, "places": Place,
                "reviews": Review, "states": State, "users": User}
    counter_objects = {}
    for i, j in classes.items():
        counter_onjects[i] = storage.count[j]

    return (jsonify(counter_objects))
