from flask import Flask,redirect,url_for,render_template,request
from models import storage
from api.v1.views import app_views
import os

app=Flask(__name__)
app.register_blueprint(app_views)
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

  
if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
    