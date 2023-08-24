"""Module that run the server"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.do_teardown_appcontext
def do_teardownZ(exception):
    """method that close the session"""
    storage.close()


if __name__ == '__main__':
    import os
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
