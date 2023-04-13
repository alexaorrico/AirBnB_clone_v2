#!/usr/bin/python3
'''
create app
'''


from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    storage.close()


if __name__ == "__main__":
    app.run(os.environ.get('HBNB_API_HOST', '0.0.0.0'),
            os.environ.get('HBNB_API_PORT', 5000), threaded=True)
