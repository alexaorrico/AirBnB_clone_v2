#!/usr/bin/python3
""" Endpoint (route) that returns the status of your API
"""
from models import storage
from api.vi.views import app_views
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_(exception):
    """ close the storage """
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
