#!/usr/bin/python3
"""
Structure of flask api
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    teardown function to close connection
    """
    storage.close()

if __name__ == "__main__":
    host_env = getenv("HBNB_API_HOST")
    port_env = getenv("HBNB_API_PORT")
    host = host_env if host_env else "0.0.0.0"
    port = int(port_env) if port_env else 5000
    app.run(host=host, port=port)

