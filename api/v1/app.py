#!/usr/bin/python
"""Starting the API"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """a handler for 404 errors that returns a JSON-formatted
    404 status code response"""
    return jsonify(error="Not found")


if __name__ == "__main__":
    try:
        app.run(host=os.getenv("HBNB_API_HOST"),
                port=int(os.getenv("HBNB_API_PORT")),
                threaded=True)
    except Exception:
        app.run(host='0.0.0.0', port=5000, threaded=True)
