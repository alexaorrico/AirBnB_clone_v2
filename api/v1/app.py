#!/usr/bin/python3
"""
Start api
First instance: return the status of your API
"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def teardown_appcont(exception):
    """Closes the session running"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """Create a handler for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")),
            threaded=True, debug=True)
