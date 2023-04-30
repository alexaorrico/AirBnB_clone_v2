#!/usr/bin/python3
"""

"""
import os
from flask import Flask
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
# Register the app_views bluepint to the app
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def close_storage(exception):
    """Close the storage connection at the end of the request"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
