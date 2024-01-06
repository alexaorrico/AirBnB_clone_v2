#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, Flask, Blueprint
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

hbnbText = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }
@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnb status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def hbnbstats():
    """Status check"""
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
