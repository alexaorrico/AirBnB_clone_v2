#!/usr/bin/python3
"""run flask server"""
from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def reset(error):
    """reload data"""
    storage.close()


if __name__ == "__main__":
    try:
        app.run(host=os.getenv('HBNB_API_HOST'),
                port=os.getenv('HBNB_API_PORT'),
                threaded=True)
    except:
        app.run(host='0.0.0.0', port=5000, threaded=True)
