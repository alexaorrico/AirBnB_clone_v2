#!/usr/bin/python3
"""create a variable app, instance of Flask"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(app_views, url_prefix='/myapp')

@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage resource at the end."""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """handles 404 error by returning a JSON."""
    error_dict = {"error": "Not found"}
    status_code = 404
    return jsonify(error_dict), status_code


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

