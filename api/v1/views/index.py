#!/usr/bin/python3
"""Define routes for blueprint"""

from api.v1.views import app_views
from flask import jsonify
<<<<<<< HEAD
from models import storagei
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
=======
from models import storage
>>>>>>> adcf563bc8a2103965790b0d19936676e151b983


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of application"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
<<<<<<< HEAD
    """Retrieve count of bjcts in storage"""
=======
    """Retrieve count of objects in storage"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
>>>>>>> adcf563bc8a2103965790b0d19936676e151b983

    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    json_dict = {}

    for name, cls in classes.items():
        json_dict.update({name: storage.count(cls)})

    return jsonify(json_dict)
