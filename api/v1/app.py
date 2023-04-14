#!/usr/bin/python3
"""
    Main file of API,
    he store the Flask app and run the api
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def page_not_found(error):
    """
        Return a JSON error message. 
        This is used to display an error when the request cannot be found.

        @param error - The error that was encountered. Can be None.
        @return The JSON error message with the error message in it
    """
    return jsonify({"error": "Not found"})


def teardown_db(exception):
    """
     Clean up after test. This is called at the end of each test and cleans up the database.

     @param exception - The exception that caused the test to fail. This is used to provide context to the failure
    """
    storage.close()


# Run the app with the default port 5000 threaded true
if __name__ == '__main__':
    app.run(
        host= getenv('HBNB_API_HOST', '0.0.0.0'),
        port= getenv('HBNB_API_PORT', '5000'),
        threaded=True
    )

