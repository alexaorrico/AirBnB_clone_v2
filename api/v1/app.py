#!/usr/bin/python3
"""App.py is the entry point, all the routes of
the Blueprints will be registered here and this App.py
is the one who will execute the application"""

from flask import Flask, jsonify, make_response
from models import storage
# here we import our blueprint app_views
from api.v1.views import app_views

app = Flask(__name__)

# Now as we know the Blueprints are not an application
# so they have to be registered in our app.py
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    response = make_response(jsonify({"error": "Not found"}), 404)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
