#!/usr/bin/python3
"""App.py is the entry point, all the routes of
the Blueprints will be registered here and this App.py
is the one who will execute the application"""

from flask import Flask, jsonify
from models import storage
# here we import our blueprint app_views
from api.v1.views import app_views

app = Flask(__name__)

# Now as we know the Blueprints are not an application
# so they have to be registered in our app.py
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
