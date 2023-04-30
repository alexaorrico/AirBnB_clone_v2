from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    return jsonify(status="OK")

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each object by type
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
