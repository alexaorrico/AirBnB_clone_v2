#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': "Not found"}), 404


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=getenv("HBNB_API_PORT", default="5000"))
    """if hb_port and hb_host:
        app.run(
            host=getenv(hb_host),
            port=getenv(hb_port),
            threaded=True)
    else:
        app.run(
            host="0.0.0.0",
            port="5000",
            threaded=True)
    """
