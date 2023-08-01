#!/usr/bin/python3
"""registers the blueprint to your flask instance app"""
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# app.url_map.strict_slashes = False


@app.teardown_appcontext
def tearDown(self):
    """closes a query after every session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Define host and port
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
