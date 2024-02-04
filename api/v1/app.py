#!/usr/bin/python3
""" flask app set up"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(exception=None):
    """ close db session after each request"""

    storage.close()


@app.errorhandler(404)
def error_page(e):
    """ error page"""

    obj = {"error": "Not found"}
    return jsonify(obj), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
