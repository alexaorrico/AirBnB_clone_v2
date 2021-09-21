#!/usr/bin/python3
""" Flask app with cors module   """

from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_request(exception=None):
    """Closes the connection when the execution finish"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ Flask main function """
    my_host = environ.get("HBNB_API_HOST")
    my_port = environ.get("HBNB_API_PORT")
    app.run(host=my_host, port=my_port, threaded=True, debug=True)
