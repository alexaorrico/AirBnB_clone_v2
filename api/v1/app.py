#!/usr/bin/python3
"""Module for app endpoint of the views module of v1 of the RESTful API"""

from api.v1.views import app_views, storage
from flask import jsonify
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask_cors import CORS
from os import getenv
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage engine"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Returns a 404 error in JSON format"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
