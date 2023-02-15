#!/usr/bin/python3
"""
This is an endpoint to return the status of the API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ as env

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """ Closes the database request after each request"""
    storage.close()


if __name__ == "__main__":
    host = env.get("HBNB_API_HOST", "0.0.0.0")
    port = int(env.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
