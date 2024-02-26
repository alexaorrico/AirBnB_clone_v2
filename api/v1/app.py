#!/usr/bin/python3
"""register blueprint"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os


app = Flask(__name__)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close db session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port)
