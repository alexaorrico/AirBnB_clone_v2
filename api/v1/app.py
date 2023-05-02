#!/usr/bin/python3
""" first endpoint (route) will be to return the status of your API """


from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
