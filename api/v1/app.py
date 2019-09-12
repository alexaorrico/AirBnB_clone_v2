#!/usr/bin/python3
"""
starts a Flask web application:
web application must be listening on 0.0.0.0, port 5000
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception=None):
    """closes or otherwise deallocates the resource"""
    storage.close()

if __name__ == '__main__':
    app.run(port=int(getenv("HBNB_API_PORT")),
            host=getenv("HBNB_API_HOST"), threaded=True)
