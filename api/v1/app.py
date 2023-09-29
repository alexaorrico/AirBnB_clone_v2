#!/usr/bin/python3
""" Starting the API """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(error):
    """ Close the storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error 404: Resouce not found """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ The main function """
    port = environ.get('HBNB_API_PORT')
    host = environ.get('HBNB_API_HOST')
    if not port:
        port = '5000'
    if not host:
        host = '0.0.0.0'
    app.run(host=host, port=port, threaded=True)
