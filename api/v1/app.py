#!/usr/bin/python3
"""Main application script"""


from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error=None):
    '''Terminates the storage engine connection'''
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    '''Handles 404 errors and returns a JSON response'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
