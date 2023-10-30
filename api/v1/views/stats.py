from api.v1.views import app_views
from flask import jsonify
from models import storage

# Define the count method here
def count(cls=None):
    all_class = storage.all()
    count = 0
    if not cls:
        for obj_class in all_class.values():
            count += len(obj_class)
    else:
        count = len(all_class.get(cls, {}).values())

    return count

@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    stats_data = {
        "amenities": count("Amenity"),
        "cities": count("City"),
        "places": count("Place"),
        "reviews": count("Review"),
        "states": count("State"),
        "users": count("User")
    }

    return jsonify(stats_data)
