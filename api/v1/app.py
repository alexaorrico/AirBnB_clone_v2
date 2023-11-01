#!/usr/bin/python3
"""
This module contains the app
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
