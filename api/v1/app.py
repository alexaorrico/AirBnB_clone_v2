#!/usr/bin/python3
"""API part of the AirBnB clone project"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os
from api.v1.views.states import *

app = Flask(__name__)

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# environment variables
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNT_API_PORT', 5000)

# declare a method to handle @app.teardown_appcontext
# that calls storage.close()


@app.teardown_appcontext
def teardown_db(exception):
    """
    method to close the SQLAlchemy session after each request
    """

    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """Runs the flask app"""

    app.run(host=host, port=port, threaded=True)
