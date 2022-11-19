#!/usr/bin/python3

"""Flask App that integrates with AirBnB static HTML Template"""
from api.v1.views import app_views
from models import storage
from flask import Flask
import os

app = Flask(__name__)

app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def close():
    """
    this method calls .close() 
    the current SQLAlchemy Session
    """
    storage.close()


if __name__ == '__main__':
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)
