#!/usr/bin/python3
"""INDEX.PY

    Route Status
"""


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models import user, city, state, amenity, review, place


@app_views.route('/status', strict_slashes=False)
def index():
    """
     Return status of API.
     Used to check if user is allowed to access API

     @return jsonified version of status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
     Count how many records exist in the database.
     This is useful for determining if a query is valid or not.

     @return 200 if everything worked 400 if something went wrong with the
    """

    return jsonify({
        "amenities": storage.count(amenity),
        "cities": storage.count(city),
        "places": storage.count(place),
        "reviews": storage.count(review),
        "state": storage.count(state),
        "users": storage.count(user),
    })
