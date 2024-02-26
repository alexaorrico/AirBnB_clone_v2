#!/usr/bin/python3
"""
flask app blueprint registration
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os

app = Flask(__name__)

app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    calls close methods after each method
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port)
