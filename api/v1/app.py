#!/usr/bin/python3
"""It's time to start your API. Your first endpoint\
(route) will be to return the status of your API"""


from api.v1.views import app_views
from models import storage
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def err_not_fnd():
    return jsonify("error": "Not found")


@app.teardown_appcontext
def close(self):
    """closes session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
