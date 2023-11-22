#!/usr/bin/python3
"""Create and teardown a Flask instance."""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """Close database session"""
    storage.close()


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
