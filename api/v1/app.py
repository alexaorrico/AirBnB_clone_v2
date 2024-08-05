#!/usr/bin/python3
"""
Creating a Flask application
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS  # Import CORS from flask_cors
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

# Initialize CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def exit(exception):
    ''' close the API if an unexpected error occurs '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 error response"""
    response = {"error": "Not found"}
    return make_response(jsonify(response), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
