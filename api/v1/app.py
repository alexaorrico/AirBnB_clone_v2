#!/usr/bin/python3
"""
This is the main Flask application for your API.
"""


from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage on teardown."""
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
