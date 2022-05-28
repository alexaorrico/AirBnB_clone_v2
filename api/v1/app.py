#!/usr/bin/python3
"""Start Flask App"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close(current):
    """Close session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
