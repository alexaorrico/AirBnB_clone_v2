#!/usr/bin/python3
"""App Module
"""
from flask import Flask, jsonify
from models import storage
from os import environ
from api.v1.views import app_views
from flask import make_response

app = Flask(__name__)
app.register_blueprint(app_views)
@app.teardown_appcontext
def close_storage(self):
    """"""
    self.storage.close()


@app.errorhandler(404)
def not_found(error):
    """"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """"""
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
