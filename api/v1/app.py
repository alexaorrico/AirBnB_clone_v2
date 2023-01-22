#!/usr/bin/python3
"""Flask app module"""
from flask import Flask, request
from models import storage
from api.v1.views import app_views
from api.v1.views import state_views
from flask import make_response, jsonify
from os import getenv

app = Flask(__name__)
app_views.register_blueprint(state_views)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """Release Resources"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    if  (request.path.startswith('/api/v1/states/') and 
         request.method == 'POST'):
        return ('Not a JSON')
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    hst = getenv('HBNB_API_HOST')
    prt = getenv('HBNB_API_PORT')
    HOST = '0.0.0.0' if not hst else hst
    PORT = 5000 if not prt else prt
    app.run(host=HOST, port=PORT, threaded=True)
