#!/usr/bin/python3
""" api """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

@app.teardown_appcontext
def v3(error):
    """ close storage"""
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}

if __name__ == "__main__":
    """ run appi"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host=host, port=port, threaded=True)
