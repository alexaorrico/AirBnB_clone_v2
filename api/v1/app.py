#!/usr/bin/python3
'''
Main file to run program
'''
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
from flasgger import Swagger


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
swagger = Swagger(app)


@app.teardown_appcontext
def teardown_db(exception):
    '''Close connection'''
    storage.close()


@app.errorhandler(404)
def error_notfound(error):
    """featuring 404 error page
    response: json file"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    try:
        host = getenv('HBNB_API_HOST')
    except Exception as e:
        host = "0.0.0.0"

    try:
        port = getenv('HBNB_API_PORT')
    except Exception as e:
        port = 5000

    app.run(host=host, port=port, debug=True)
