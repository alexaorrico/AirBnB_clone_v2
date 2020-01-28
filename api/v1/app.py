#!/usr/bin/pyhton3
"""It’s time to start an API!"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """A method to handle @app.teardown_appcontext that calls storage.close"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True, debug=True)
