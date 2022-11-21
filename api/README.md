## API
1. Create a folder api at the root of the project with an empty file __init__.py
2. Create a folder v1 inside api:
* create an empty file __init__.py
* create a file app.py:
* create a variable app, instance of Flask
* import storage from models
* import app_views from api.v1.views
* register the blueprint app_views to your Flask instance app
* declare a method to handle @app.teardown_appcontext that calls storage.close()
* inside if __name__ == "__main__":, run your Flask server (variable app) with:
* host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
* port = environment variable HBNB_API_PORT or 5000 if not defined
* threaded=True

3. Create a folder views inside v1:
* create a file __init__.py:
* import Blueprint from flask doc
* create a variable app_views which is an instance of Blueprint (url prefix must be /api/v1)
* wildcard import of everything in the package api.v1.views.index => PEP8 will complain about it, don’t worry, it’s normal and this file (v1/views/__init__.py) won’t be check.
* create a file index.py
* import app_views from api.v1.views
* create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)