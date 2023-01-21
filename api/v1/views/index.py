from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    amenities_cnt = storage.count("Amenity")
    cities_cnt = storage.count("City")
    places_cnt = storage.count("Place")
    reviews_cnt = storage.count("Review")
    states_cnt = storage.count("State")
    users_cnt = storage.count("User")

    stats = {
        "amenities": amenities_cnt, 
        "cities": cities_cnt, 
        "places": places_cnt, 
        "reviews": reviews_cnt, 
        "states": states_cnt, 
        "users": users_cnt,
    }

    return jsonify(stats)