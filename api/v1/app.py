#!/usr/bin/python3
"""This module has the blueprints"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from api.v1.views.index import api_v1_stats

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.register_blueprint(api_v1_stats)


@app.error_handler(404)
def handle_error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown(exception):
    """
    calls the close() method
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
