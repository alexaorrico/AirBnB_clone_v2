#!/usr/bin/python3
"""
Initiates a Flask app
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(e):
    """ error handler function """
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """ closes the storage on teardown  """
    storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0,0')
    PORT = getenv('HBNB_API_PORT', '5000')

    app.run(host=HOST, port=PORT, threaded=True, debug=True)
