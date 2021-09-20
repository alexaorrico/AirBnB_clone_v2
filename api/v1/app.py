#!/usr/bin/python3
"""App Module
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask import make_response

app = Flask(__name__)
app.register_blueprint(app_views)
@app.teardown_appcontext
def close_storage(self):
    """"""
    self.storage.close()


@app.errorhandler(404)
def not_found(error):
    """"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
