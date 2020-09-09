#!/usr/bin/python3
"""
Module For start a Flask web application
"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    storage.close()


if __name__ == '__main__':
    host_env = getenv('HBNB_API_HOST')
    port_env = getenv('HBNB_API_PORT')
    app.run(host=host_env, port=port_env)
