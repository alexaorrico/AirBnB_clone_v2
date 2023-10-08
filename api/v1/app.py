#!/usr/bin/python3
""" API """

import os
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """ Handles storage calls """
    storage.close()


@app.errorhandler(404)
def not_found(error):
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
    app.run(host=host, port=port, threaded=True)
