#!/usr/bin/python3
''' Starting flask! '''


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(context):
    ''' Calling close for app '''
    storage.close()


@app.errorhandler(404)
def pageNotFound(error):
    ''' Handles 404 error page'''
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'), port=int(
        getenv('HBNB_API_PORT', '5000')), threaded=True)
