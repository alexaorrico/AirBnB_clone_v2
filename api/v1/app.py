#!/usr/bin/python3
"""app module """
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv
from flask import make_response
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def td_contxt(exception):
    """call storage close metoh"""
    storage.close()


@app.errorhandler(404)
def resource_not_found(error):
    """hadle 404 error and return a message"""
    return make_response({'error': 'Not found'}, 404)


if __name__ == "__main__":
    """ entry point """
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default='5000'),
            threaded=True)
