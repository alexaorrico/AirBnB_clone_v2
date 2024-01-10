#!/usr/bin/python3
""" Flask App """
import os
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={'/*': {'origins': "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """ teardown method for storage """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ handling error page """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=Trueg)
