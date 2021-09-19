#!usr/bin/python3
'''
AirBnB API
'''


from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(msg=None):
    '''
    Teardown close calls close method
    '''
    storage.close()

if __name__ == "__main__":
    '''
    Run app with host and port environment variables, if none use default
    '''

    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)

    app.run(host, int(port), threaded=True)
