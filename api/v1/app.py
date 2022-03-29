#!/usr/bin/python3
"""
create a variable app, instance of Flask
register the blueprint app_views to your Flask instance app
"""
from models import storage
from views import app_views
from os import getenv
from flask import Flask
from flask_cors import CORS
from flask.json import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")
host_name = getenv('HBNB_API_HOST')
port_name = getenv('HBNB_API_PORT')

@app.teardown_appcontext
def teardown(self):
    """
    closes session
    """
    storage.close()

@app.errorhandler(404)
def not_found_404(e):
    """
    returns error
    """
    return jsonify(error='Not found'), 404

if __name__ == 'main':
    app.run(host=host_name, port=port_name, threaded=True)
