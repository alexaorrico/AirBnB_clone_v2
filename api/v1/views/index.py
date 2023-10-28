#!/usr/bin/python3
""" Create a Route -> (/status) on the Object """
from flask import Response, jsonify
from api.v1.views import app_views
from models import storage
from models.engine.db_storage import classes

@app_views.route('/status', strict_slashes=False)
def status():
    """ Status ->  That Return a JSON -> ('OK') """
    return jsonify({'status': 'OK'})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """ In Storage -> Retrieve the count of objects """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    json_dict = {}

    for name, clas in classes.items():
        json_dict.update({name: storage.count(clas)})
    return jsonify(json_dict)
