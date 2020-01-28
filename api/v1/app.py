#!/usr/bin/python3
""" Starts a Flask web application with blueprints """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ App closes storage when closed """
    storage.close()

@app.errorhandler(404)
def error_handler(err):
    """ This method handle the error 404 response """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded='True', debug=True)
