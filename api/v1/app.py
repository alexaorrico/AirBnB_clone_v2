#!/usr/bin/python3
""""""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


env_host = getenv('HBNB_API_HOST')
if not env_host:
    env_host = "0.0.0.0"
env_port = getenv('HBNB_API_PORT')
if not env_port:
    env_port = "5000"


@app.teardown_appcontext
def teardown_db():
    """Closes storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=env_host, port=env_port, threaded=True)
