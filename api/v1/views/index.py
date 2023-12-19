
#!/usr/bin/python3
"""Index Script"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """API Status"""
    return jsonify({'status': "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """Get the numbers by type"""
    classes = [Amenity, City, Place, Review, State, User]
    name = ["amenities", "cities", "places", "reviews", "states", "users"]

    obj_nums = {}
    for i in range(len(classes)):
        obj_nums[name[i]] = storage.count(classes[i])

    return jsonify(obj_nums)
