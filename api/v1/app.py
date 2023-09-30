#!/usr/bin/python3
# V1 app

from flask import Flask, request
from markupsafe import escape

from models import storage
from api.v1.views import app_views


app = Flask(__name__)

#  register a blueprint 'app_views'
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_db(exception):
    """ Clone MySQL session """
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
