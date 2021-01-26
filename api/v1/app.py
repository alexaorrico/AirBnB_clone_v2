#!/usr/bin/python3
"""x"""

from models import storage
from flask import Flask
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def page_not_found(err=None):
    """x"""
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def tear(err=None):
    """rip and"""
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, threaded=True)
