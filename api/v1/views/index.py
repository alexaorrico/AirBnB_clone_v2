#!/usr/bin/python3
<<<<<<< HEAD
"""Define routes for blueprint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of application
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieve count of objects in storage
    """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    json_dict = {}

    for name, cls in classes.items():
        json_dict.update({name: storage.count(cls)})

    return jsonify(json_dict)
=======
""" Creates the index file """
from flask import jsonify
from api.v1.views import app_views

@app.views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of blueprint API ""
    return jsonify({status: "OK"})
>>>>>>> 7f463f781d2f2c16e360fbc7e590cd9adf4bcd7c
