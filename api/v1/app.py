#!/usr/bin/python3
"""
Sets up Flask app API
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv

# Create a variable app, instance of Flask
# register blueprint app_views to your Flask instance app
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Closes the app"""
    storage.close()


# registering error handler for code 404
@app.errorhandler(404)
def page_not_found(error):
    not_found = {'error': 'Not found'}
    return not_found


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True)
