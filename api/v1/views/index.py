#!/usr/bin/python3
""" The status code for the api """


from api.v1.views import app_views
from flask import jsonify


# Route to get status of the API
@app_views.route('/status')
def status():
    """Retrieves the status of the API
    """
    return jsonify({"status": "OK"})


# Route to get statistics about the stored object.
@app_views.route('/stats')
def count():
    """Retrieves statistics about the stored objects.
    """
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.user import User
    from models.review import Review

    # Count objects of each type using the storage's count method
    c_amenities = storage.count(Amenity)
    c_cities = storage.count(City)
    c_places = storage.count(Place)
    c_reviews = storage.count(Review)
    c_states = storage.count(State)
    c_users = storage.count(User)

    # Return the counts in JSON format
    return jsonify({
        "amenities": c_amenities,
        "cities": c_cities,
        "places": c_places,
        "reviews": c_reviews,
        "states": c_states,
        "users": c_users
    })
