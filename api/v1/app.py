#!/usr/bin/python3
'''Model blueprint'''
from models import storage
from api.v1.views import app_views
import flask
from os import getenv


app = flask.Flask(__name__)
app.register_blueprint(app_views)


@app.route('/', strict_slashes=False)
def index():
    """Hello HBNB!"""
    return ('Hello HBNB!')


@app.teardown_appcontext
def teardown(self):
    '''Method that calls storage.close()'''
    storage.close()

if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0.'
    if HBNB_API_PORT is None:
        HBNB_API_PORT = '5000'
    app.run(debug=True, threaded=True, host=HBNB_API_HOST, port=HBNB_API_PORT)
