#!/usr/bin/python3
'''Entry point Airbnb_clone_v3 api calls'''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(self):
    '''This method is call after every request is made to a route
    main functionality is to close the storage session.
    '''
    storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default='5000'),
        threaded=True
    )
