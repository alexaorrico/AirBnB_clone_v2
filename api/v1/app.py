#!/usr/bin/python3
'''Flask server app var'''

from models import storage
from api.v1.views import app_views
from flask import Flask

# Create a variable app, instance from flask
app = Flask(__name__)

# register the blueprint app_views to your app
app.register_blueprint(app_views)


# method to handle the close of the app
@app.teardown_appcontext
def donw_method():
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
