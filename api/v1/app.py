#!/usr/bin/python3
"""
0x05. AirBnB clone - RESTful API
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

#  Get host and port from environ if defined
if environ.get('HBNB_API_HOST') is None:
    HBNB_API_HOST = "0.0.0.0"
else:
    HBNB_API_HOST = environ.get('HBNB_API_HOST')
if environ.get('HBNB_API_PORT') is None:
    HBNB_API_PORT = 5000
else:
    HBNB_API_PORT = environ.get('HBNB_API_PORT')


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """Close any active SQLAlchemy sessions"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error 404 """
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
