#!/usr/bin/python3
"""
blue print module for api
contain all the routes
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

"""create a variable app, instance of Flask"""
app = Flask(__name__)

"""register the blueprint app_views to your Flask instance app"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """
    Teardown the application context.
    """
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, threaded=True, host=host, port=port)
