#!/usr/bin/python3
'''
Start the airbnb ap
'''

from flask import Flask, jsonify 
from models import storage
from api.v1.views import app_views 
from getenv import env


app = Flask(__name__)


@app.register_blueprint(app_views)
@app.teardown_appcontext
def teardown(error):
    '''
    Teardown
    '''
    return storage.close()


if __name__ == '__main__':
    app.run(getenv('HBNB_API_HOST'),getenv('HBNB_API_PORT'),threaded=True)
