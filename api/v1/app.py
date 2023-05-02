#!/usr/bin/python3
""" Start flask app """


import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """page not found error handling"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    # Set the host, port using environ variables, or defaults if not defined
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask server with threaded=True to allow concurrent requests
    app.run(host=host, port=port, threaded=True)
