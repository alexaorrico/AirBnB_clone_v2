#!/usr/bin/python3
"""
api/v1/app.py
"""

from flask import Flask
from os import getenv
from api.v1 import app_views
from models import storage

app = Flask(__name__)

# Register blueprints
app.register_blueprint(app_views)

# Handle teardown
@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
