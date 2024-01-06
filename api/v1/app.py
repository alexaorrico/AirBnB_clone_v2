#!/usr/bin/python3
""" Flask app for aibrnb clone"""
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """closes current sqlalchemy session"""
    storage.close()


host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', '5000')


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
