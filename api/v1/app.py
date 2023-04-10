#!/usr/bin/python3
"""
script that starts a Flask web application.
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
import os

"""create a variable app, instance of Flask"""
app = Flask(__name__)

"""register the blueprint app_views"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Closes the connection to the database"""
    storage.close()


if __name__ == "__main__":

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True)
