#!/usr/bin/python3
"""This is a flask appplication"""

from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(error):
    """This method is for clean-up"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """This is a custom 404 error"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)
