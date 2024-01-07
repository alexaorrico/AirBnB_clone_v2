#!/usr/bin/python3
'''The app module'''
from models import storage
from flask import Flask, make_response
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def onTearDownContext(self):
    ''' Handles app clean up '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    ''' Handles 404 error '''
    return make_response({'error': 'Not found'}, 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    # print(app.url_map)
    app.run(
        host=host if host else '0.0.0.0',
        port=port if port else 5000,
        threaded=True,
        # debug=True
    )
