#!/usr/bin/python3
"""app.py"""
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from flask import Flask
from os import getenv
from flask import jsonify
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_appcontext(error):
    """teardown_appcontext"""
    storage.close()



if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
