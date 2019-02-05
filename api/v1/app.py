#!/usr/bin/python3
"""
Root file of our application
"""
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """Tear down method to close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return custom message for 404 errors"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host_ip = '0.0.0.0'
    port_num = 5000
    if getenv('HBNB_API_HOST'):
        host_ip = getenv('HBNB_API_HOST')
    if getenv('HBNB_API_PORt'):
        port_num = int(getenv('HBNB_API_PORT'))
    app.run(host=host_ip, port=port_num, threaded=True)
