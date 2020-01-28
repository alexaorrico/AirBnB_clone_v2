#!/usr/bin/python3
"""
Build Flask Application
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """Closes storage on teardown"""
    storage.close()


if __name__ == "__main__":
    env_host = getenv('HBNB_API_HOST', default="0.0.0.0")
    env_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=env_host, port=env_port, threaded=True, debug=True)
