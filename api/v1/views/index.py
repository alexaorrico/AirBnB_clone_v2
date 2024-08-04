from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    amenities_count = storage.count("Amenity")
    cities_count = storage.count("City")
    places_count = storage.count("Place")
    reviews_count = storage.count("Review")
    states_count = storage.count("State")
    users_count = storage.count("User")
    
    print("Amenities count:", amenities_count)
    print("Cities count:", cities_count)
    print("Places count:", places_count)
    print("Reviews count:", reviews_count)
    print("States count:", states_count)
    print("Users count:", users_count)
    
    stats = {
        "amenities": amenities_count,
        "cities": cities_count,
        "places": places_count,
        "reviews": reviews_count,
        "states": states_count,
        "users": users_count
    }
    return jsonify(stats)
