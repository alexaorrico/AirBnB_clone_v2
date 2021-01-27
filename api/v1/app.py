#!/usr/bin/python3
"""Status of the api """

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask import make_response

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def stoclose(self):
    """call storage.close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default='5000'),
            threaded=True)
