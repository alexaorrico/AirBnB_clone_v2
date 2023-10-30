#!/usr/bin/python3
"""
Script uses blueprint object for routing the application
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(error):
    """
    function closes the db when called
    """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """
    404 error handler
    """
    return make_response(jsonify({"error": 'Not found'}), 404)


if __name__ == '__main__':
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000

    app.run(host=host, port=port, threaded=True)  # type: ignore
