#!/usr/bin/python3
"""It’s time to start an API!"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """A method to handle @app.teardown_appcontext that calls storage.close"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """create a handler for 404 errors that returns a JSON-formatted 404
    status code response"""
    error = {"error": "Not found"}
    return make_response(jsonify(error), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
