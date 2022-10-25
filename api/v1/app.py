#!/usr/bin/python3
"""
Flask App that intergrates with AirBnB static.
"""
from os import getenv
from flask import Flask, make_response, jsonify, Blueprint
from models import storage
from api.v1.views import app_views

# Flask Application: app
app = Flask(__name__)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(Exception):
    """after every request, this method calls .close()
        on the current SQLAlchemy session
    """
    storage.close()

if __name__ == "__main__":
    """
        Main Flask app.
    """
    app.run(host=host, port=port, threaded= True)