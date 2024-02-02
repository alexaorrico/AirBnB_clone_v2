#!/usr/bin/python3
""" The status code for the api """


from api.v1.views import app_views
from flask import jsonify


# Route to get status of the API
@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    """Retrieves the status of the API
    """
    return jsonify({"status": "OK"})


# Route to get statistics about the stored object.
@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def get_stats():
    """Retrieves statistics about the stored objects.
    """
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.user import User
    from models.review import Review

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
