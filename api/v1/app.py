#!/usr/bin/python3
'''Returning the status of API'''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import environ
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    '''teardown - method to call storage.close()'''
    storage.close()


if __name__ == '__main__':
    env_host = environ.get('HBNB_API_HOST', '0.0.0.0')
    env_port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=env_host, port=env_port, threaded=True)
