#!/usr/bin/python3
""" starts api """


from flask import Flask

from api.v1.views import app_views
from models import storage

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(self):
    """ not sure if it should be exception or self """
    """ a method that calls storage.close """
    storage.close()

@app.pagenotfound(404)
def custom_404(error):
    """ Returns JSON 404 """
    return jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    if not HBNB_API_HOST:
        HBNB_API_HOST = "0.0.0.0"
    if not HBNB_API_PORT:
        HBNB_API_PORT = "5000"
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
