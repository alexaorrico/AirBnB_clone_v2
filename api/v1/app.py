#!/usr/bin/python3
'''
This module is basis for the Flask API.
It contains the teardown and run configuration.
'''


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    '''Closes the connection to storage when it is finished.'''
    storage.close()


if __name__ == '__main__':
    app_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    app_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=app_host, port=app_port, threaded=True, debug=True)
