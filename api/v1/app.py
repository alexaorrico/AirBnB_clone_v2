#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(stiven):
    """teardown function"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
