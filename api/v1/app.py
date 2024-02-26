#!/usr/bin/python3
"""
starts a flask web application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def removed_db(exception):
    """
    remove every db session connection to the database
    db is been created in every subsequent calls
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
