#!/usr/bin/python3
"""
initialization of app
"""

from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from flasgger import Swagger
from models import storage
from os import getenv



app = Flask(__name__)
app.config['JSON_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(app_views)
cors = CORS(
    app,
    resources={
        r"api/v1/*": {"origins": "0.0.0.0"}
    }
)


@app.teardown_app_context
def shutdown(exception):
    """
    closes storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return error in JSON and status"""
    return make_response(jsonify({"error": "Not Found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone RESTFUL API',
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
