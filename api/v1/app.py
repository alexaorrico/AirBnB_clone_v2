#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(err):
    """closes storage session"""
    storage.close()

if __name__ == "__main__":
    app.run(
        host=os.environ.get('HBNB_API_HOST'),
        port=os.getenv('HBNB_API_PORT'),
        threaded=True
    )
