    #!/usr/bin/python3
""" API Status and Object Statistics """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ Endpoint to get the status of the API """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def objects_statistics():
    """ Endpoint to retrieve the number of each object type """
    object_types = [Amenity, City, Place, Review, State, User]
    type_names = ["amenities", "cities", "places", "reviews", "states", "users"]

    object_counts = {}
    for i in range(len(object_types)):
        object_counts[type_names[i]] = storage.count(object_types[i])

    return jsonify(object_counts)
