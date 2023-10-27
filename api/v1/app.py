#!usr/bin/python3
"""
API V1 task 2
"""
from flask import Flask, jsonify
# import storage from models
from models import storage
# import env from to read env vars
from os import getenv
# make an instance on Flask class and assign
# it to app variable
app = Flask(__name__)
# import app_views from api.v1.views
from api.v1.views import app_views
# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# enable json pretty printed
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# disable strict _slashes globally
# by default it was on
app.url_map.strict_slashes = False
# declare a method to handle @app.teardown_appcontext
# that calls storage.close()


@app.teardown_appcontext
def close_strg(error):  # don't forget this argument to handle errors
    """
    closes storage session
    """
    if error:
        app.logger.error(
            f"Unhandled exception on teardown:{error}")
    storage.close()


if __name__ == "__main__":
    # run your Flask server (variable app) with:
    # host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
    # port = environment variable HBNB_API_PORT or 5000 if not defined
    # threaded=True
    app.run(host=getenv('HBNB_API_HOST', default="0.0.0.0"),
            port=int(getenv('HBNB_API_PORT', default=5000)),
            threaded=True
            )
