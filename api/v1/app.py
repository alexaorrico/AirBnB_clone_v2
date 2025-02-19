#!/usr/bin/python3
"""Creates a flask application"""

import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# flask app instance
app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# initialize CORS with the app instsnce
CORS(app, resources={r"/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown(exception):
    """closes current SQLAlchemy session"""
    storage.close()

def page_not_found(error):
    """Handles 404 not found errors"""
    return({'error': 'Not found'}), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True )
