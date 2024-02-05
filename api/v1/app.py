#!/usr/bin/python3
"""start flask api"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage():
    """closes storage"""
    storage.close()

if __name__ == "__main__":
    port = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') is not None else '0.0.0.0'
    host = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') is not None else '5000'
    app.run(threaded=True, port=port, host=host)
