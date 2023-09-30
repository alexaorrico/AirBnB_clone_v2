#!/usr/bin/python3
"""
Start API
"""

from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def downtear(self):
    """ Close the storage when the app context is torn down  """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Define a custom 404  error handler"""
    return ({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
