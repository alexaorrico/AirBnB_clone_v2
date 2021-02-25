#!/usr/bin/python3
"""web app creation module"""

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(err=None):
    """page not found error handler"""
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def tear(err=None):
    """app teardown function"""
    storage.close()

if __name__ == "__main__":
    h = getenv("HBNB_API_HOST")
    if not h:
        h = "0.0.0.0"
    p = getenv("HBNB_API_PORT")
    if not p:
        p = 5000
    app.run(host=h, port=p, threaded=True)
