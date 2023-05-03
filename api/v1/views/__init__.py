#!/usr/bin/python3
"""
Initializes a Flask web application
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

from api.v1.views.users import *
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *

from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(self):
    """Removes the current SQLAlchemy session"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
