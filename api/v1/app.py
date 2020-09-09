#!/usr/bin/python3
""" Web APP """

from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import environ, getenv


app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv("HBNB_API_HOST") if "HBNB_API_HOST" in environ else "0.0.0.0"
port = getenv("HBNB_API_PORT") if "HBNB_API_PORT" in environ else 5000


@app.teardown_appcontext
def teardown_storage(self):
    """ Teardown storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ not found 404 """
    response = jsonify({
        'error': 'Not found'
    })
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True, debug=True)
