#!/usr/bin/python3
"""
Flask App
"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__)
# Register the blueprint containing the API routes
app.register_blueprint(app_views)
# Setup CORS to allow requests from any origin
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


# Teardown app context to close database connection
@app.teardown_appcontext
def close_db(error):
    """
    Closes storage
    """
    storage.close()


@app.errorhandler(404)
def not_found():
    """
    404 error handler
    """
    return make_response(jsonify({"error": "Not found"}), 404)


app.config['SWAGGER'] = {
    'title': 'AirBnB clone v3 Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """
    Main Function
    """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    # set default host and port
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
