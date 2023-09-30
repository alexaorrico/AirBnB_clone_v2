#!/usr/bin/python3

"""
A flask application
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


# create a Flask application
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Close the storage on teardown."""
    storage.close()


if __name__ == '__main__':
    """run flask server"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
