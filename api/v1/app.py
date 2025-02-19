#!/usr/bin/python3
<<<<<<< HEAD
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
=======
""" 
This script imports a Blueprint path and runs Flask 
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import getenv
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'HBNB REST API',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)


@app.teardown_appcontext
def teardown_session(exception):
    """ 
    This method closes the storage session 
    """
>>>>>>> c18aee22ec56a82b2b1c541e9134627845d1d329
    storage.close()


@app.errorhandler(404)
def not_found(error):
<<<<<<< HEAD
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
=======
    """ 
    This method returns JSON response with a 404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' 
    if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 
    if not HBNB_API_PORT else HBNB_API_PORT
>>>>>>> c18aee22ec56a82b2b1c541e9134627845d1d329
    app.run(host=host, port=port, threaded=True)
