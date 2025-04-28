#!/usr/bin/python3
"""
initializes a basic Flask app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# instantiates Flask
app = Flask(__name__)

# register blueprints
app.register_blueprint(app_views)

@app.teardown_appcontext(Exception)
def teardown_db(exception):
    """closes storage engine"""
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host and port:
        app.run(host=host, port=port, threaded=True, debug=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
