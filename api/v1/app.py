#!/usr/bin/python3
"""
    This script starts a Flask web application
"""
import os

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.register_blueprint(app_views)


cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.route('/', strict_slashes=False)
def index():
    """returns Hello HBNB!"""
    return 'Hello HBNB!'


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error(e):
    """Handler for 404 errors"""
    return jsonify(dict(error="Not found")), 404


app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}
Swagger(app)

if __name__ == "__main__":
    env_host = os.getenv('HBNB_API_HOST')
    env_port = os.getenv('HBNB_API_PORT')
    app.run(host=env_host if env_host else '0.0.0.0',
            port=env_port if env_port else 5000,
            threaded=True)
