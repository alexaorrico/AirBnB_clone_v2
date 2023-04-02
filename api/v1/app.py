#!/usr/bin/python3
"""App"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv as env


"""creating a instance of Flask & register blueprint"""
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = env('HBNB_API_HOST', default='0.0.0.0')
    port = env('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
