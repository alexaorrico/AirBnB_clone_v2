#!/usr/bin/python3
"""ALX SE Flask Api Module."""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception=None):
    """Close current session."""
    storage.close()


if __name__ == '__main__':
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=HOST, port=PORT, threaded=True)
