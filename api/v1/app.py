#!/usr/bin/python3
'''task 4'''
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tearitup():
    """turrupboii"""
    storage.close()


def start_flask():
    """ start flask """
    app.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'),
            threaded=True)


"""404 error handler"""


@app.errorhandler(404)
def not_found_error(error):
    return Blueprint({'error': 'Not found'}), 404

if __name__ == "__main__":
    start_flask()
