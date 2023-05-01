# (301) 0x05. AirBnB clone - RESTful API
Foundations > Higher-level programming > AirBnB clone

---

### Project author
Guillaume Salva

### Assignment dates
09-04-2020 to 09-11-2020

### Description
Building the third iteration of a website cloning the basic features of the [`airbnb.com` main page, circa 2014-2017](https://web.archive.org/web/20170206112507/https://www.airbnb.com/).

Using Flask in Python to create an API that can query the storage engine and serve JSON reponses.

## General requirements

### Python
* Interpreter conditions:
  * Ubuntu 14.04 LTS
  * python3 (version 3.4.3)
* First line of executable scripts will be `#!/usr/bin/python3`
* Compliance with linter:
  * `pep8` (version 1.7.*) (now known as `pycodestyle`)
* Docstrings are expected to follow the [Google style guide](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html):
  * Per module (`python3 -c 'print(__import__("my_module").__doc__)'`)
  * Per class (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
  * Per function
    * both inside a class (`python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
    * and outside a class (`python3 -c 'print(__import__("my_module").my_function.__doc__)'`)
* Test scripts will typically not be in same directory as the task solutions, use `export PYTHONPATH='.'` before running test scripts from project directory to allow includes
* Unit tests will be required on some projects:
  * using the [unittest module](https://docs.python.org/3.4/library/unittest.html#module-unittest)
  * located in a `tests/` folder, with a file structure mimicing that of your project, but with a `test_` prefix added to all file/directory names
  * tests should be capable of being run with `python3 -m unittest discover tests`, or individually per file with `python3 -m unittest <test file>`

### Install Flask
```bash
$ pip3 install Flask
```

---

## Mandatory Tasks

### :white_check_mark: 0. Restart from scratch!
But once again, let’s work on a new codebase.

For this project you will fork this [codebase](https://github.com/alexaorrico/AirBnB_clone_v2.git):
* Update the repository name to `AirBnB_clone_v3`
* Update the `README.md`:
    * Add yourself as an author of the project
    * Add new information about your new contribution
    * Make it better!
* If you’re the owner of this codebase, create a new repository called `AirBnB_clone_v3` and copy over all files from `AirBnB_clone_v2`

### :white_check_mark: 1. Never fail!
Since the beginning we’ve been using the unittest module, but do you know why unittests are so important? Because when you add a new feature, you refactor a piece of code, etc… you want to be sure you didn’t break anything.

The following requirements must be met for your project:
* all current tests must pass (don’t delete them…)
* add new tests as much as you can (tests are mandatory for some tasks)

```bash
~/AirBnB_v3$ python3 -m unittest discover tests 2>&1 | tail -1
OK
~/AirBnB_v3$ HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
OK
~/AirBnB_v3$ 
```

### :white_check_mark: 2. Code review
Like “tests”, code review is the base of all software development.

What is a code review?

Code review helps developers learn the code base, as well as help them learn new technologies and techniques that grow their skill sets.

When a developer is finished working on an issue, another developer looks over the code and considers questions like:
* Are there any obvious logic errors in the code?
* Looking at the requirements, are all cases fully implemented?
* Are the new automated tests sufficient for the new code? Do existing automated tests need to be rewritten to account for changes in the code?
* Does the new code conform to existing style guidelines?

For this project, you will need to review a peer’s pull request on the branch `storage_get_count` (which will be made for task 3), and then accept the pull request, with your review in the comments.

What we expect:
* a file `code_review.txt`, containing the GitHub username of the student you reviewed (ex: If you did the review of JohnDoe, `code_review.txt` must contain `JohnDoe`)
* The code review must be done on GitHub, in the comments for the pull request:
    * the pull request must be created from the branch `storage_get_count` by a peer
    * only the reviewer can approve the pull request
    * don’t delete the branch storage_get_count after approval
* The comments must contain at least one useful comment:
    * questions about the piece of code, if it’s difficult to understand
    * style issues
    * error handling
    * duplicate code
    * potential bugs
    * potential efficiency issues
    * typographical errors

We are all human, we all make mistakes, typos, etc… another developer will always find something in your code.

File(s): [`code_review.txt`](./code_review.txt)

### :white_check_mark: 3. Improve storage
Update `DBStorage` and `FileStorage`, adding two new methods. All changes should be done in the branch `storage_get_count`:

A method to retrieve one object:
* Prototype: `def get(self, cls, id):`
    * `cls`: class
    * `id`: string representing the object ID
* Returns the object based on the class and its ID, or `None` if not found

A method to count the number of objects in storage:
* Prototype: `def count(self, cls=None):`
    * `cls`: class (optional)
* Returns the number of objects in storage matching the given class. If no class is passed, returns the count of all objects in storage.

Don’t forget to add new tests for these 2 methods on each storage engine.

For this task, you must make a pull request on GitHub.com, and ask at least one of your peer to review and merge it.

Please do not delete this branch, a manual review for grading will be done using this branch.

File(s): [`models/engine/db_storage.py`](./models/engine/db_storage.py) [`models/engine/file_storage.py`](./models/engine/file_storage.py) [`tests/test_models/test_engine/test_db_storage.py`](./tests/test_models/test_engine/test_db_storage.py) [`tests/test_models/test_engine`](./tests/test_models/test_engine) [`/test_file_storage.py`](.//test_file_storage.py)

### :white_check_mark: 4. Status of your API
Your first endpoint (route) will be to return the status of your API:
* Create a folder `api` at the root of the project with an empty file `__init__.py`
* Create a folder `v1` inside `api`:
    * create an empty file `__init__.py`
    * create a file `app.py`:
        * create a variable `app`, instance of `Flask`
        * import `storage` from `models`
        * import `app_views` from `api.v1.views`
        * register the blueprint `app_views` to your Flask instance `app`
        * declare a method to handle `@app.teardown_appcontext` that calls `storage.close()`
        * inside if `__name__ == "__main__":`, run your Flask server (variable `app`) with:
            * host = environment variable `HBNB_API_HOST` or `0.0.0.0` if not defined
            * port = environment variable `HBNB_API_PORT` or `5000` if not defined
            * `threaded=True`
* Create a folder `views` inside `v1`:
    * create a file `__init__.py`:
        * import `Blueprint` from `flask`
        * create a variable `app_views` which is an instance of `Blueprint` (url prefix must be `/api/v1`)
        * wildcard import of everything in the package `api.v1.views.index` => PEP8 will complain about it, but you can disregard in this case for `v1/views/__init__.py`
    * create a file `index.py`
        * import `app_views` from `api.v1.views`
        * create a route `/status` on the object `app_views` that returns a JSON: `"status": "OK"`

File(s): [`api/__init__.py`](./api/__init__.py) [`api/v1/__init__.py`](./api/v1/__init__.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py) [`pi/v1/views/index.py`](./pi/v1/views/index.py) [`api/v1/app.py`](./api/v1/app.py)

### :white_check_mark: 5. Some stats?
Create an endpoint that retrieves the number of each objects by type:
* In `api/v1/views/index.py`
* Route: `/api/v1/stats`
* You must use the newly added `count()` method from `storage`

File(s): [`api/v1/views/index.py`](./api/v1/views/index.py)

### :white_check_mark: 6. Not found
Designers are often really creative when they have to design a “404 page”, but this will be different, because you won’t use HTML and CSS, but JSON!

In `api/v1/app.py`, create a handler for 404 errors that returns a JSON-formatted 404 status code response. The content should be: `"error": "Not found"`

File(s): [`api/v1/app.py`](./api/v1/app.py)

### :white_check_mark: 7. State
Create a new view for `State` objects that handles all default RESTFul API actions:
* In the file `api/v1/views/states.py`
* You must use `to_dict()` to retrieve an object into a valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all `State` objects: `GET /api/v1/states`

Retrieves a `State` object: `GET /api/v1/states/<state_id>`
* If the `state_id` is not linked to any `State` object, raise a 404 error

Deletes a `State` object: `DELETE /api/v1/states/<state_id>`
* If the `state_id` is not linked to any `State` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a State: `POST /api/v1/states`
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key name, raise a 400 error with the message `Missing name`
* Returns the new `State` with the status code 201

Updates a `State` object: `PUT /api/v1/states/<state_id>`
* If the `state_id` is not linked to any `State` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `State` object with all key-value pairs of the dictionary.
* Ignore keys: `id`, `created_at` and `updated_at`
* Returns the `State` object with the status code 200

File(s): [`api/v1/views/states.py`](./api/v1/views/states.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 8. City
Same as `State`, create a new view for `City` objects that handles all default RESTFul API actions:
* In the file `api/v1/views/cities.py`
* You must use `to_dict()` to serialize an object into valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all `City` objects of a `State`: `GET /api/v1/states/<state_id>/cities`
* If the `state_id` is not linked to any `State` object, raise a 404 error

Retrieves a `City` object: `GET /api/v1/cities/<city_id>`
* If the `city_id` is not linked to any `City` object, raise a 404 error

Deletes a `City` object: `DELETE /api/v1/cities/<city_id>`
* If the `city_id` is not linked to any `City` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a `City`: `POST /api/v1/states/<state_id>/cities`
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the `state_id` is not linked to any `State` object, raise a 404 error
* If the HTTP body request is not a valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key `name`, raise a 400 error with the message `Missing name`
* Returns the new `City` with the status code 201

Updates a `City` object: `PUT /api/v1/cities/<city_id>`
* If the `city_id` is not linked to any `City` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `City` object with all key-value pairs of the dictionary
* Ignore keys: `id`, `state_id`, `created_at` and `updated_at`
* Returns the `City` object with the status code 200

File(s): [`api/v1/views/cities.py`](./api/v1/views/cities.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 9. Amenity
Create a new view for `Amenity` objects that handles all default RESTFul API actions:
* In the file `api/v1/views/amenities.py`
* You must use `to_dict()` to serialize an object into valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all `Amenity` objects: `GET /api/v1/amenities`

Retrieves a `Amenity` object: `GET /api/v1/amenities/<amenity_id>`
* If the `amenity_id` is not linked to any `Amenity` object, raise a 404 error

Deletes a `Amenity` object:: `DELETE /api/v1/amenities/<amenity_id>`
* If the `amenity_id` is not linked to any `Amenity` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a `Amenity`: `POST /api/v1/amenities`
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key `name`, raise a 400 error with the message `Missing name`
* Returns the new `Amenity` with the status code 201

Updates a `Amenity` object: `PUT /api/v1/amenities/<amenity_id>`
* If the `amenity_id` is not linked to any `Amenity` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `Amenity` object with all key-value pairs of the dictionary
* Ignore keys: `id`, `created_at` and `updated_at`
* Returns the `Amenity` object with the status code 200

File(s): [`api/v1/views/amenities.py`](./api/v1/views/amenities.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 10. User
Create a new view for `User` object that handles all default RESTFul API actions:
* In the file `api/v1/views/users.py`
* You must use `to_dict()` to retrieve an object into a valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all User objects: `GET /api/v1/users`

Retrieves a `User` object: `GET /api/v1/users/<user_id>`
* If the `user_id` is not linked to any `User` object, raise a 404 error

Deletes a `User` object: `DELETE /api/v1/users/<user_id>`
* If the `user_id` is not linked to any `User` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a `User`: `POST /api/v1/users`
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key `email`, raise a 400 error with the message `Missing email`
* If the dictionary doesn’t contain the key `password`, raise a 400 error with the message `Missing password`
* Returns the new `User` with the status code 201

Updates a `User` object: `PUT /api/v1/users/<user_id>`
* If the `user_id` is not linked to any `User` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `User` object with all key-value pairs of the dictionary
* Ignore keys: `id`, `email`, `created_at` and `updated_at`
* Returns the `User` object with the status code 200

File(s): [`api/v1/views/users.py`](./api/v1/views/users.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 11. Place
Create a new view for `Place` objects that handles all default RESTFul API actions:
* In the file `api/v1/views/places.py`
* You must use `to_dict()` to retrieve an object into a valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all `Place` objects of a `City`: `GET /api/v1/cities/<city_id>/places`
* If the `city_id` is not linked to any `City` object, raise a 404 error

Retrieves a `Place` object: `GET /api/v1/places/<place_id>`
* If the `place_id` is not linked to any `Place` object, raise a 404 error

Deletes a `Place` object: `DELETE /api/v1/places/<place_id>`
* If the `place_id` is not linked to any `Place` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a `Place`: `POST /api/v1/cities/<city_id>/places`
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the `city_id` is not linked to any `City` object, raise a 404 error
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key `user_id`, raise a 400 error with the message `Missing user_id`
* If the `user_id` is not linked to any `User` object, raise a 404 error
* If the dictionary doesn’t contain the key `name`, raise a 400 error with the message `Missing name`
* Returns the new `Place` with the status code 201

Updates a `Place` object: `PUT /api/v1/places/<place_id>`
* If the `place_id` is not linked to any `Place` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `Place` object with all key-value pairs of the dictionary
* Ignore keys: `id`, `user_id`, `city_id`, `created_at` and `updated_at`
* Returns the `Place` object with the status code 200

File(s): [`api/v1/views/places.py`](./api/v1/views/places.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 12. Reviews
Create a new view for `Review` object that handles all default RESTFul API actions:
* In the file `api/v1/views/places_reviews.py`
* You must use `to_dict()` to retrieve an object into valid JSON
* Update `api/v1/views/__init__.py` to import this new file

Retrieves the list of all `Review` objects of a `Place`: `GET /api/v1/places/<place_id>/reviews`
* If the `place_id` is not linked to any `Place` object, raise a 404 error

Retrieves a `Review` object: `GET /api/v1/reviews/<review_id>`
* If the `review_id` is not linked to any Review object, raise a 404 error

Deletes a `Review` object: `DELETE /api/v1/reviews/<review_id>`
* If the `review_id` is not linked to any `Review` object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a `Review`: `POST /api/v1/places/<place_id>/reviews`
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the `place_id` is not linked to any `Place` object, raise a 404 error
* If the HTTP body request is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the dictionary doesn’t contain the key `user_id`, raise a 400 error with the message `Missing user_id`
* If the `user_id` is not linked to any `User` object, raise a 404 error
* If the dictionary doesn’t contain the key `text`, raise a 400 error with the message `Missing text`
* Returns the new `Review` with the status code 201

Updates a `Review` object: `PUT /api/v1/reviews/<review_id>`
* If the `review_id` is not linked to any `Review` object, raise a 404 error
* You must use `request.get_json` from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* Update the `Review` object with all key-value pairs of the dictionary
* Ignore keys: `id`, `user_id`, `place_id`, `created_at` and `updated_at`
* Returns the `Review` object with the status code 200

File(s): [`api/v1/views/places_reviews.py`](./api/v1/views/places_reviews.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_check_mark: 13. HTTP access control (CORS)
A resource makes a cross-origin HTTP request when it requests a resource from a different domain, or port, than the one the first resource itself serves.

Why do we need this?

Because you will soon start allowing a web client to make requests your API. If your API doesn’t have a correct CORS setup, your web client won’t be able to access your data.

With Flask, it’s really easy, you will use the class `CORS` of the module `flask_cors`.

Install with: `$ pip3 install flask_cors`

Update `api/v1/app.py` to create a `CORS` instance allowing: `/*` for `0.0.0.0`

You will update it later when you will deploy your API to production.

Now you can see this HTTP Response Header: `< Access-Control-Allow-Origin: 0.0.0.0`

File(s): [`api/v1/app.py`](./api/v1/app.py)

## Advanced Tasks

### :white_check_mark: 14. Place - Amenity
Create a new view for the link between `Place` objects and `Amenity` objects that handles all default RESTFul API actions:
* In the file `api/v1/views/places_amenities.py`
* You must use `to_dict()` to retrieve an object into a valid JSON
* Update `api/v1/views/__init__.py` to import this new file
* Depending of the storage:
    * `DBStorage`: list, create and delete `Amenity` objects from `amenities` relationship
    * `FileStorage`: list, add and remove `Amenity` ID in the list `amenity_ids` of a `Place` object

Retrieves the list of all `Amenity` objects of a `Place`: `GET /api/v1/places/<place_id>/amenities`
* If the `place_id` is not linked to any `Place` object, raise a 404 error

Deletes a `Amenity` object to a `Place`: `DELETE /api/v1/places/<place_id>/amenities/<amenity_id>`
* If the `place_id` is not linked to any `Place` object, raise a 404 error
* If the `amenity_id` is not linked to any `Amenity` object, raise a 404 error
* If the `Amenity` is not linked to the `Place` before the request, raise a 404 error
* Returns an empty dictionary with the status code 200

Link a `Amenity` object to a `Place`: `POST /api/v1/places/<place_id>/amenities/<amenity_id>`
* No HTTP body needed
* If the `place_id` is not linked to any `Place` object, raise a 404 error
* If the `amenity_id` is not linked to any `Amenity` object, raise a 404 error
* If the `Amenity` is already linked to the `Place`, return the `Amenity` with the status code 200
* Returns the `Amenity` with the status code 201

File(s): [`api/v1/views/places_amenities.py`](./api/v1/views/places_amenities.py) [`api/v1/views/__init__.py`](./api/v1/views/__init__.py)

### :white_large_square: 15. Security improvements!
Currently, the `User` object is designed to store the user password in cleartext, which is not at all secure.

To avoid that, improve the `User` object:
* Update the method `to_dict()` of `BaseModel` to remove the `password` key **except when it’s used by `FileStorage` to save data to disk**. Tips: default parameters
* Each time a new `User` object is created or password updated, the password is hashed to a [MD5](https://docs.python.org/3.4/library/hashlib.html) value
* In the database for `DBStorage`, the password stored is now hashed to a MD5 value
* In the file for `FileStorage`, the password stored is now hashed to a MD5 value

File(s): [`models/base_model.py`](./models/base_model.py) [`models/user.py`](./models/user.py)

### :white_check_mark: 16. Search
Currently, the only way to list `Place` objects is via `GET /api/v1/cities/<city_id>/places`.

Update `api/v1/views/places.py` to add a new endpoint: `POST /api/v1/places_search` that retrieves all `Place` objects depending of the JSON in the body of the request.

The JSON can contain 3 optional keys:
* `states`: list of `State` ids
* `cities`: list of `City` ids
* `amenities`: list of `Amenity` ids

Search rules:
* If the HTTP request body is not valid JSON, raise a 400 error with the message `Not a JSON`
* If the JSON body is empty or each list of all keys are empty: retrieve all `Place` objects
* If `states `list is not empty, results should include all `Place` objects for each `State` id listed
* If `cities` list is not empty, results should include all `Place` objects for each `City` id listed
* Keys `states` and `cities` are inclusive. Search results should include all `Place` objects in storage related to each `City` in every `State` listed in `states`, plus every `City` listed individually in `cities`, unless that `City` was already included by `states`.
* * Context:
        * State A has 2 cities A1 and A2
        * State B has 3 cities B1, B2 and B3
        * A1 has 1 place
        * A2 has 2 places
        * B1 has 3 places
        * B2 has 4 places
        * B3 has 5 places
    * Search: states = State A and cities = B2
    * Result: all 4 places from the city B2 and the place from the city A1 and the 2 places of the city A2 (because they are part of State A) => 7 places returned
* If amenities list is not empty, limit search results to only `Place` objects having all `Amenity` ids listed
* The key `amenities` is exclusive, acting as a filter on the results generated by `states` and `cities`, or on all `Place` if `states` and `cities` are both empty or missing.
* Results will only include `Place` objects having all listed `amenities`. If a `Place` doesn’t have even one of these `amenities`, it won’t be retrieved.

File(s): [`api/v1/views/places.py`](./api/v1/views/places.py)

### :white_large_square: 17. Documentation
Nothing better than writing tests… and documentation!

But with [Swagger](https://swagger.io/), it’s really easy!

You will use the Flask version of Swagger: [Flasgger](https://github.com/flasgger/flasgger)

How to install it: `$ pip3 install flasgger`

Add comments on each endpoint of your API, so you can view the documentation in your browser: `http://0.0.0.0:5000/apidocs`

File(s): [`api/v1/app.py`](./api/v1/app.py) [`api/v1/views/*`](./api/v1/views/*)

---

## Student team
* **Samuel Pomeroy** - [allelomorph](github.com/allelomorph)
* **Derric Donehoo** - [derric-d](github.com/derric-d)
