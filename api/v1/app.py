#!/usr/bin/python3
"""
Initialize Flask app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_storage(exception):
    """Close storage"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    debug = getenv('FLASK_ENV') == 'development'
    app.run(host=host, port=int(port), debug=debug, threaded=True)
