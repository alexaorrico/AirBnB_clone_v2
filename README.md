General
What REST means
[Disconnected...]
What CORS means
What is an API
What is a REST API
What are other type of APIs
Which is the HTTP method to retrieve resource(s)
Which is the HTTP method to create a resource
Which is the HTTP method to update resource
Which is the HTTP method to delete resource
How to request REST API

0. Restart from scratch!
mandatory
No no no! We are already too far in the project to restart everything.

But once again, let�~@~Ys work on a new codebase.

For this project you will fork this codebase:

Update the repository name to AirBnB_clone_v3
Update the README.md:
Add yourself as an author of the project
Add new information about your new contribution
Make it better!
If you�~@~Yre the owner of this codebase, create a new repository called AirBnB_clone_v3 and copy over all files from AirBnB_clone_v2

1. Never fail!
Since the beginning we�~@~Yve been using the unittest module, but do you know why unittests are so important? Because when you add a new feature, you refactor a piece of code, etc�~@� you want to be sure you didn�~@~Yt break anything.

At Holberton, we have a lot of tests, and they all pass! Just for the Intranet itself, there are:

5,213 assertions (as of 08/20/2018)
13,061 assertions (as of 01/25/2021)
The following requirements must be met for your project:

all current tests must pass (don’t delete them…)
add new tests as much as you can (tests are mandatory for some tasks)
                                            
2. Improve storage
mandatory
Update DBStorage and FileStorage, adding two new methods. All changes should be done in the branch storage_get_count:

A method to retrieve one object:

Prototype: def get(self, cls, id):
cls: class
id: string representing the object ID
Returns the object based on the class and its ID, or None if not found
A method to count the number of objects in storage:

Prototype: def count(self, cls=None):
cls: class (optional)
Returns the number of objects in storage matching the given class. If no class is passed, returns the count of all objects in storage.
Don’t forget to add new tests for these 2 methods on each storage engine.
For this task, you must make a pull request on GitHub.com, and ask at least one of your peer to review and merge it.

3. Status of your API
mandatory
It’s time to start your API!

Your first endpoint (route) will be to return the status of your API:
In another terminal:
Magic right? (No need to have a pretty rendered output, it’s a JSON, only the structure is important)

Ok, let starts:

Create a folder api at the root of the project with an empty file __init__.py
Create a folder v1 inside api:
create an empty file __init__.py
create a file app.py:
create a variable app, instance of Flask
import storage from models
import app_views from api.v1.views
register the blueprint app_views to your Flask instance app
declare a method to handle @app.teardown_appcontext that calls storage.close()
inside if __name__ == "__main__":, run your Flask server (variable app) with:
host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
port = environment variable HBNB_API_PORT or 5000 if not defined
threaded=True
Create a folder views inside v1:
create a file __init__.py:
import Blueprint from flask doc
create a variable app_views which is an instance of Blueprint (url prefix must be /api/v1)
wildcard import of everything in the package api.v1.views.index => PEP8 will complain about it, don’t worry, it’s normal and this file (v1/views/__init__.py) won’t be check.
create a file index.py
import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)

4. Some stats?
mandatory
Create an endpoint that retrieves the number of each objects by type:

In api/v1/views/index.py
Route: /api/v1/stats
You must use the newly added count() method from storage

5. Not found
mandatory
Designers are really creative when they have to design a “404 page”, a “Not found”… 34 brilliantly designed 404 error pages

Today it’s different, because you won’t use HTML and CSS, but JSON!

In api/v1/app.py, create a handler for 404 errors that returns a JSON-formatted 404 status code response. The content should be: "error": "Not found"

6. State
mandatory
Create a new view for State objects that handles all default RESTFul API actions:

In the file api/v1/views/states.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all State objects: GET /api/v1/states

Retrieves a State object: GET /api/v1/states/<state_id>

If the state_id is not linked to any State object, raise a 404 error
Deletes a State object:: DELETE /api/v1/states/<state_id>

If the state_id is not linked to any State object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a State: POST /api/v1/states

You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
Returns the new State with the status code 201
Updates a State object: PUT /api/v1/states/<state_id>

If the state_id is not linked to any State object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
Update the State object with all key-value pairs of the dictionary.
Ignore keys: id, created_at and updated_at
Returns the State object with the status code 200

7. City
mandatory
Same as State, create a new view for City objects that handles all default RESTFul API actions:

In the file api/v1/views/cities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all City objects of a State: GET /api/v1/states/<state_id>/cities

If the state_id is not linked to any State object, raise a 404 error
Retrieves a City object. : GET /api/v1/cities/<city_id>

If the city_id is not linked to any City object, raise a 404 error
Deletes a City object: DELETE /api/v1/cities/<city_id>

If the city_id is not linked to any City object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a City: POST /api/v1/states/<state_id>/cities

You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the state_id is not linked to any State object, raise a 404 error
If the HTTP body request is not a valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
Returns the new City with the status code 201
Updates a City object: PUT /api/v1/cities/<city_id>

If the city_id is not linked to any City object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
Update the City object with all key-value pairs of the dictionary
Ignore keys: id, state_id, created_at and updated_at
Returns the City object with the status code 200

8. Amenity
mandatory
Create a new view for Amenity objects that handles all default RESTFul API actions:

In the file api/v1/views/amenities.py
You must use to_dict() to serialize an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Amenity objects: GET /api/v1/amenities

Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Amenity: POST /api/v1/amenities

You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
Returns the new Amenity with the status code 201
Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>

If the amenity_id is not linked to any Amenity object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
Update the Amenity object with all key-value pairs of the dictionary
Ignore keys: id, created_at and updated_at
Returns the Amenity object with the status code 200

9. User
mandatory
Create a new view for User object that handles all default RESTFul API actions:

In the file api/v1/views/users.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all User objects: GET /api/v1/users

Retrieves a User object: GET /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
Deletes a User object:: DELETE /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a User: POST /api/v1/users

You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key email, raise a 400 error with the message Missing email
If the dictionary doesn’t contain the key password, raise a 400 error with the message Missing password
Returns the new User with the status code 201
Updates a User object: PUT /api/v1/users/<user_id>

If the user_id is not linked to any User object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP body request to a dictionary
If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
Update the User object with all key-value pairs of the dictionary
Ignore keys: id, email, created_at and updated_at
Returns the User object with the status code 200

10. Place
mandatory
Create a new view for Place objects that handles all default RESTFul API actions:

In the file api/v1/views/places.py
You must use to_dict() to retrieve an object into a valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Place objects of a City: GET /api/v1/cities/<city_id>/places

If the city_id is not linked to any City object, raise a 404 error
Retrieves a Place object. : GET /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
Deletes a Place object: DELETE /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Place: POST /api/v1/cities/<city_id>/places

You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the city_id is not linked to any City object, raise a 404 error
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
If the user_id is not linked to any User object, raise a 404 error
If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
Returns the new Place with the status code 201
Updates a Place object: PUT /api/v1/places/<place_id>

If the place_id is not linked to any Place object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
Update the Place object with all key-value pairs of the dictionary
Ignore keys: id, user_id, city_id, created_at and updated_at
Returns the Place object with the status code 200

11. Reviews
mandatory
Create a new view for Review object that handles all default RESTFul API actions:

In the file api/v1/views/places_reviews.py
You must use to_dict() to retrieve an object into valid JSON
Update api/v1/views/__init__.py to import this new file
Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews

If the place_id is not linked to any Place object, raise a 404 error
Retrieves a Review object. : GET /api/v1/reviews/<review_id>

If the review_id is not linked to any Review object, raise a 404 error
Deletes a Review object: DELETE /api/v1/reviews/<review_id>

If the review_id is not linked to any Review object, raise a 404 error
Returns an empty dictionary with the status code 200
Creates a Review: POST /api/v1/places/<place_id>/reviews

You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the place_id is not linked to any Place object, raise a 404 error
If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
If the user_id is not linked to any User object, raise a 404 error
If the dictionary doesn’t contain the key text, raise a 400 error with the message Missing text
Returns the new Review with the status code 201
Updates a Review object: PUT /api/v1/reviews/<review_id>

If the review_id is not linked to any Review object, raise a 404 error
You must use request.get_json from Flask to transform the HTTP request to a dictionary
If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
Update the Review object with all key-value pairs of the dictionary
Ignore keys: id, user_id, place_id, created_at and updated_at
Returns the Review object with the status code 200

12. HTTP access control (CORS)
mandatory
A resource makes a cross-origin HTTP request when it requests a resource from a different domain, or port, than the one the first resource itself serves.

Read the full definition here

Why do we need this?

Because you will soon start allowing a web client to make requests your API. If your API doesn’t have a correct CORS setup, your web client won’t be able to access your data.

With Flask, it’s really easy, you will use the class CORS of the module flask_cors.

How to install it: $ pip3 install flask_cors

Update api/v1/app.py to create a CORS instance allowing: /* for 0.0.0.0

You will update it later when you will deploy your API to production.

Now you can see this HTTP Response Header: < Access-Control-Allow-Origin: 0.0.0.0 

AUTHORS: SALOME ESSIEN, PATRICE OKLOU
