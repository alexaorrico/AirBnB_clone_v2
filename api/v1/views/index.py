#!/usr/bin/python3
"""API routes for status and stats endpoints."""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns status of API."""
    return jsonify({"status": "OK"})


@app.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Returns count of each type of object in database."""
    count_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(count_stats)

if __name__ == '__main__':
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'),
            threaded=True)
