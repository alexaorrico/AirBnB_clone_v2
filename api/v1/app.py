#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
# Way to organize Flask application into smaller, reusable components.
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ closes the storage @app.teardown_appcontext is
     used to perform tasks that should be executed after
     each request to ensure proper resource
     management and prevent resource leaks"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """ Returns a JSON formatted 404 status code res"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    if host is None:
        host = '0.0.0.0'
    port = getenv("HBNB_API_PORT")
    if port is None:
        port = 5000
    app.run(host=host, port=port, threaded=True)
