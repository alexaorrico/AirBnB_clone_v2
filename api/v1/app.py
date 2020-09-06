#!/usr/bin/python3
"""
    Task 4 ASDFKJA;LDFKA;LDFK;AF
"""
from models import storage
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearthatmotherfuckerdown(self):
    """ tear that shit down """
    storage.close()


@app.errorhandler(404)
def dudewermypge(e):
    """ dude, where's my page """
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
