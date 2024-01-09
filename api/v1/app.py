#!/usr/bin/python3
"""starts a flask app for our api"""

from flask import Flask, jsonify, make_response
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(exception):
    """closes the app and frees up resources"""
    storage.close()
print(app.url_map)

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


value_host = os.getenv('HBNB_API_HOST')
value_port = os.getenv('HBNB_API_PORT')
if value_host is not None:
    host = value_host
else:
    host = '0.0.0.0'

if value_port is not None:
    port = value_port
else:
    port = 5000

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
