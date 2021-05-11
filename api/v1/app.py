#!/usr/bin/python3
""" Starts Flask web app """

from flask import Flask
app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """ closes storage on teardown """
    storage.close()

@app.errorhandler(404)
def not_found_404(err):
    """returns page not found 404 error"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
