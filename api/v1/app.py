#!/usr/bin/python3
"""create a variable app, instance of Flask"""

from flask import Flask
from api.v1.views import app_views
from models import storage
import os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.register_blueprint(app_views, url_prefix='/myapp')

@app.teardown_appcontext
def close_storage(exception=None):
    """Close the storage resource at the end of the request."""
    if hasattr(g, 'storage'):
        g.storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """handles 404 error by returning a JSON error response"""
    error_dict = {"error": "Not found"}
    status_code = 404
    return jsonify(error_dict), status_code


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

