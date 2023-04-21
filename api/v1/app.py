#!/usr/bin/env python3
"""
Flask App that integrates with AirBnb static HTML Template
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(self):
    """
    Calls storage.close() on app context teardown
    """
    storage.close()


if __name__ == '__main__':
    app.run(
        host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
        port=os.getenv('HBNB_API_PORT', '5000'),
        threaded=True
    )
