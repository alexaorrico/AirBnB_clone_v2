#!/usr/bin/python3
"""
Starts the flask app.py
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


host_env = getenv("HBNB_API_HOST", "0.0.0.0")
port_env = getenv("HBNB_API_PORT", "5000")

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_con(error):
    """closes the database connection"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host_env, port=port_env, threaded=True)
