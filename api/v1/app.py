#!/usr/bin/python3
"""
initializes a basic Flask app
"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views, states_views, cities_views, amenities_views

# instantiates Flask
app = Flask(__name__)
app.url_map.strict_slashes = False

# register blueprints
app.register_blueprint(app_views)
app.register_blueprint(states_views)
app.register_blueprint(cities_views)
app.register_blueprint(amenities_views)


@app.teardown_appcontext(Exception)
def teardown_db(exception):
    """closes storage engine"""
    storage.close()


@app.errorhandler(404)
def error_handler(e):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host and port:
        app.run(host=host, port=port, threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
