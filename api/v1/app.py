#!/usr/bin/python3
"""
Flask API v1
"""
from flask import Flask
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)

app.register_blueprint(app_views)
swagger = Swagger(app)

host = getenv('HBNB_API_HOST') or 5000
port = getenv('HBNB_API_PORT') or '0.0.0.0'

cors = CORS(app, resources={"*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """Calls close session storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error routine"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
