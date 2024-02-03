#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    returns a JSON: "status": "OK"
    """
    return {"status": "OK"}


@app_views.route("/stats")
def stats():
    """
    returns a JSON: "amenity": <number of amenity objects>
    "cities": <number of city objects>
    "places": <number of place objects>
    "reviews": <number of review objects>
    "states": <number of state objects>
    "users": <number of user objects>
    """
    from models import storage

    return {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }


if __name__ == "__main__":
    app_views.run(host="0.0.0.0", port="5000")
