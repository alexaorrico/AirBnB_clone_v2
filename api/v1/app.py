#!/usr/bin/python3
""" App module
"""


import os
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False



@app.teardown_appcontext
def tear_down(self):
    """ Calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def page_not_found_err(error):
    """ Return 404 not found error page
    """
    return jsonify(error='Not found'), 404



if __name__ == '__main__':
    if not os.getenv('HBNB_API_HOST'):
        host = '0.0.0.0'
    else:
        host = os.getenv('HBNB_API_HOST')
    if not os.getenv('HBNB_API_PORT'):
        port = 5000
    else:
        port = os.getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
