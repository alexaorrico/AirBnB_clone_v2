#!/usr/bin/python3
"""
initializing flask app
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.do_teardown_appcontext()


def tear_down(data):
    """
    tear down app
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ 404 error handler """
    return make_response(jsonify({"error": "Not found"}), 404)   
  
 
if __name__ == "__main__":
    """ Main Function """
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
