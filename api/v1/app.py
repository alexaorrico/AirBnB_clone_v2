  #!/usr/bin/python3
  """
  api/v1/app.py
  Main entry point for the Flask application.
   """
  import os
   from flask import Flask
   from flask_cors import CORS Blueprint, jsonify, make_response
   from models import storage
  from api.v1.views import app_views
  
  
  app = Flask(__name__)
  CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
 
  app.register_blueprint(app_views)
  app.url_map.strict_slashes = False
 
 
 @app.teardown_appcontext
 def close_storage(exception):
     """
     Teardown app context: close storage.
     """
     storage.close()
 
 
 @app.errorhandler(404)
 def not_found(error):
     """
     Custom error handler for 404 Not Found.
     """
     return {"error": "Not found"}, 404
 
 
 if __name__ == "__main__":
     host = os.getenv('HBNB_API_HOST', '0.0.0.0')
     port = int(os.getenv('HBNB_API_PORT', 5000))
     app.run(host=host, port=port, threaded=True

