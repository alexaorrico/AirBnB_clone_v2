#!/usr/bin/python3
"""first endpoint (route) will be to return the status of your API"""
from os import getenv
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_db(exception):
    """method to close the database"""

    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
