#!/usr/bin/python3
"""
This module has the blueprints
its also runs the Flask app
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views, state_bp, cities_bp, amenities_bp
from api.v1.views import users_bp
import os
app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(state_bp)
app.register_blueprint(cities_bp)
app.register_blueprint(amenities_bp)
app.register_blueprint(users_bp)


@app.teardown_appcontext
def teardown(exception):
    """
    calls the close() method
    """
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    """
    handles 404 error
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
