#!/usr/bin/python3
"""app module"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

"""register the blueprint app_views to your Flask instance app"""
@app.teardown_appcontext
def close_storage(exception):
    """close storage connection"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=host, port=port, threaded=True)
