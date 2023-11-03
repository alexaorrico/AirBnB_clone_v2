#!/usr/bin/python3
"""for the following files"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(err):
    """Teardown the application"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """loads a custom 404 page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    port = getenv("HBNB_API_PORT")
    host = getenv("HBNB_API_HOST")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
