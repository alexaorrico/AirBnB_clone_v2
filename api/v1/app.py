#!/usr/bin/python3
"""
endpoint (route) will be to return the status of your API
"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception=None):
    """
    Function to be called when the application context is torn down.
    Closes the SQLAlchemy session.
    """
    return storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
