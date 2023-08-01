#!/usr/bin/python3
"""Flask web service API"""


from flask import Flask, make_response, jsonify
from flask_cors import CORS
import os

from models import storage
from api.v1.views import app_views  # Blueprint


app = Flask(__name__)
"""Flask web app instace"""

app.url_map.strict_slashes = False
"""set strict slashes on routes"""

app.register_blueprint(app_views)
"""Register app_views as blueprint to app"""

CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
"""Set up CORS for app"""


@app.teardown_appcontext
def close_storage(error=None):
    """ Called when application context is torn down"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a not found repond error"""

    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=(os.getenv('HBNB_API_HOST', '0.0.0.0')),
            port=(int(os.getenv('HBNB_API_PORT', '5000'))),
            threaded=True)
