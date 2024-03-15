#!/usr/bin/python3
from flask import Flask
from models import storage
# hasn't been created yet
from api.v1.views import app_views 


app = Flask(__name__)

# register blueprint app_views to app ?

@app.teardown_appcontext
def teardown():
    storage.close()



if __name__ == "__main__":
    # need to set these to HBNB_API_HOST and HBNB_API_PORT
    app.run(host='0.0.0.0', port=5000)
    # threaded=true, what does that mean?

