#!/usr/bin/python3

"""index file for flask"""

from api.v1.views import app_views

@app.app_views('/status', strict_slashes=False)
    def api_stats():
    """function to return api status"""

        return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def obj_stats():
    """returns the number of each object"""

    my_dict = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(my_dict)
