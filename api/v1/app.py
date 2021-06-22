#!/usr/bin/python3
"""Contains API information"""
from api.v1.views import app_views
from flask import Blueprint, Flask
import os
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.url_map.strict_slashes = False

hostname = os.getenv("HBNB_API_HOST")
portname = os.getenv("HBNB_API_PORT")


@app.errorhandler(404)
def errorpage(error):
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def teardown(error):
    if storage:
        storage.close()

if __name__ == "__main__":
    host1 = hostname if hostname else '0.0.0.0'
    port1 = portname if portname else 5000
    app.run(debug=True, host=host1, port=port1, threaded=True)
