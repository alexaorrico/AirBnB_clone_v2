#!/usr/bin/python3

from models import storage
from flask import Flask, Blueprint, jsonify
import os

# Create a Flask app instance
app = Flask(__name__)

# Create a Blueprint named app_views with the URL prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Define the /status endpoint
@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

# Define the /stats endpoint
@app_views.route('/stats', methods=['GET'])
def count():
    count_dict = {
        "users": storage.count("User"),
        "places": storage.count("Place"),
        "states": storage.count("State"),
        "cities": storage.count("City"),
        "amenities": storage.count("Amenity"),
        "reviews": storage.count("Review")
    }
    return jsonify(count_dict)

# Register the app_views Blueprint to the app
app.register_blueprint(app_views)

# Define the teardown_appcontext function to close the database connection after each request
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == "__main__":
    # Run the Flask server
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
