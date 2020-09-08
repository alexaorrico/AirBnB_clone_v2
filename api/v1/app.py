#!/usr/bin/python3
"""
 Test cities access from a state
"""

from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def not_found(error):
    """ 404 error """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardowndb(exception):
    """ session close """
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'), threaded=True)
