#!/usr/bin/python3
"""
First endpoint (route) that will be to return the status of the API
"""

import os
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Return a custom 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
