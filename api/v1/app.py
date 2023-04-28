#!/usr/bin/python3
'''Start our api'''
import os
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def destro(error):
    '''method to handle teardown'''
    if hasattr(storage, 'close'):
        storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
if __name__ == "__main__":
    my_host = os.getenv("HBNB_API_HOST") if os.getenv("HBNB_API_HOST") else '0.0.0.0'
    my_port = os.getenv("HBNB_API_PORT") if os.getenv("HBNB_API_PORT") else '5000'
    app.run(host=my_host, port=my_port, threaded=True)
