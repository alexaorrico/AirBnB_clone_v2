# AirBnB Clone - The Console
The console is the first segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level programming. The goal of AirBnB project is to eventually deploy our server a simple copy of the AirBnB Website(HBnB). A command interpreter is created in this segment to manage objects for the AirBnB(HBnB) website.

#### Functionalities of this command interpreter:
* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database etc...
* Do operations on objects (count, compute stats, etc...)
* Update attributes of an object
* Destroy an object

## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Authors](#authors)
* [License](#license)

## Environment
This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)

## Installation
* Clone this repository: `git clone "https://github.com/alexaorrico/AirBnB_clone.git"`
* Access AirBnb directory: `cd AirBnB_clone`
* Run hbnb(interactively): `./console` and enter command
* Run hbnb(non-interactively): `echo "<command>" | ./console.py`

## File Descriptions
[console.py](console.py) - the console contains the entry point of the command interpreter. 
List of commands this console current supports:
* `EOF` - exits console 
* `quit` - exits console
* `<emptyline>` - overwrites default emptyline method and does nothing
* `create` - Creates a new instance of`BaseModel`, saves it (to the JSON file) and prints the id
* `destroy` - Deletes an instance based on the class name and id (save the change into the JSON file). 
* `show` - Prints the string representation of an instance based on the class name and id.
* `all` - Prints all string representation of all instances based or not on the class name. 
* `update` - Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file). 

#### `models/` directory contains classes used for this project:
[base_model.py](/models/base_model.py) - The BaseModel class from which future classes will be derived
* `def __init__(self, *args, **kwargs)` - Initialization of the base model
* `def __str__(self)` - String representation of the BaseModel class
* `def save(self)` - Updates the attribute `updated_at` with the current datetime
* `def to_dict(self)` - returns a dictionary containing all keys/values of the instance

Classes inherited from Base Model:
* [amenity.py](/models/amenity.py)
* [city.py](/models/city.py)
* [place.py](/models/place.py)
* [review.py](/models/review.py)
* [state.py](/models/state.py)
* [user.py](/models/user.py)

#### `/models/engine` directory contains File Storage class that handles JASON serialization and deserialization :
[file_storage.py](/models/engine/file_storage.py) - serializes instances to a JSON file & deserializes back to instances
* `def all(self)` - returns the dictionary __objects
* `def new(self, obj)` - sets in __objects the obj with key <obj class name>.id
* `def save(self)` - serializes __objects to the JSON file (path: __file_path)
* ` def reload(self)` -  deserializes the JSON file to __objects

#### `/tests` directory contains all unit test cases for this project:
[/test_models/test_base_model.py](/tests/test_models/test_base_model.py) - Contains the TestBaseModel and TestBaseModelDocs classes
TestBaseModelDocs class:
* `def setUpClass(cls)`- Set up for the doc tests
* `def test_pep8_conformance_base_model(self)` - Test that models/base_model.py conforms to PEP8
* `def test_pep8_conformance_test_base_model(self)` - Test that tests/test_models/test_base_model.py conforms to PEP8
* `def test_bm_module_docstring(self)` - Test for the base_model.py module docstring
* `def test_bm_class_docstring(self)` - Test for the BaseModel class docstring
* `def test_bm_func_docstrings(self)` - Test for the presence of docstrings in BaseModel methods

TestBaseModel class:
* `def test_is_base_model(self)` - Test that the instatiation of a BaseModel works
* `def test_created_at_instantiation(self)` - Test created_at is a pub. instance attribute of type datetime
* `def test_updated_at_instantiation(self)` - Test updated_at is a pub. instance attribute of type datetime
* `def test_diff_datetime_objs(self)` - Test that two BaseModel instances have different datetime objects

[/test_models/test_amenity.py](/tests/test_models/test_amenity.py) - Contains the TestAmenityDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_amenity(self)` - Test that models/amenity.py conforms to PEP8
* `def test_pep8_conformance_test_amenity(self)` - Test that tests/test_models/test_amenity.py conforms to PEP8
* `def test_amenity_module_docstring(self)` - Test for the amenity.py module docstring
* `def test_amenity_class_docstring(self)` - Test for the Amenity class docstring

[/test_models/test_city.py](/tests/test_models/test_city.py) - Contains the TestCityDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_city(self)` - Test that models/city.py conforms to PEP8
* `def test_pep8_conformance_test_city(self)` - Test that tests/test_models/test_city.py conforms to PEP8
* `def test_city_module_docstring(self)` - Test for the city.py module docstring
* `def test_city_class_docstring(self)` - Test for the City class docstring

[/test_models/test_file_storage.py](/tests/test_models/test_file_storage.py) - Contains the TestFileStorageDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_file_storage(self)` - Test that models/file_storage.py conforms to PEP8
* `def test_pep8_conformance_test_file_storage(self)` - Test that tests/test_models/test_file_storage.py conforms to PEP8
* `def test_file_storage_module_docstring(self)` - Test for the file_storage.py module docstring
* `def test_file_storage_class_docstring(self)` - Test for the FileStorage class docstring

[/test_models/test_place.py](/tests/test_models/test_place.py) - Contains the TestPlaceDoc class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_place(self)` - Test that models/place.py conforms to PEP8.
* `def test_pep8_conformance_test_place(self)` - Test that tests/test_models/test_place.py conforms to PEP8.
* `def test_place_module_docstring(self)` - Test for the place.py module docstring
* `def test_place_class_docstring(self)` - Test for the Place class docstring

[/test_models/test_review.py](/tests/test_models/test_review.py) - Contains the TestReviewDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_review(self)` - Test that models/review.py conforms to PEP8
* `def test_pep8_conformance_test_review(self)` - Test that tests/test_models/test_review.py conforms to PEP8
* `def test_review_module_docstring(self)` - Test for the review.py module docstring
* `def test_review_class_docstring(self)` - Test for the Review class docstring

[/test_models/state.py](/tests/test_models/test_state.py) - Contains the TestStateDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_state(self)` - Test that models/state.py conforms to PEP8
* `def test_pep8_conformance_test_state(self)` - Test that tests/test_models/test_state.py conforms to PEP8
* `def test_state_module_docstring(self)` - Test for the state.py module docstring
* `def test_state_class_docstring(self)` - Test for the State class docstring

[/test_models/user.py](/tests/test_models/test_user.py) - Contains the TestUserDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_user(self)` - Test that models/user.py conforms to PEP8
* `def test_pep8_conformance_test_user(self)` - Test that tests/test_models/test_user.py conforms to PEP8
* `def test_user_module_docstring(self)` - Test for the user.py module docstring
* `def test_user_class_docstring(self)` - Test for the User class docstring


## Examples of use
```
vagrantAirBnB_clone$./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) all MyModel
** class doesn't exist **
(hbnb) create BaseModel
7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) all BaseModel
[[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}]
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}
(hbnb) destroy BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
** no instance found **
(hbnb) quit
```

## Bugs
No known bugs at this time. 

---
## For this project, students are expected to look at these concepts:

* [Rest API]
* Rest API concept page
* Learn REST: A RESTful Tutorial
* Designing a RESTful API with Python and Flask
* HTTP access control (CORS)
* Flask cheatsheet
* What are Flask Blueprints, exactly?
* Flask
* Modular Applications with Blueprints
* Flask tests
* Flask-CORS

---
## Learning Objectives
At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

* What REST means
* What API means
* What CORS means
* What is an API
* What is a REST API
* What are other type of APIs
* Which is the HTTP method to retrieve resource(s)
* Which is the HTTP method to create a resource
* Which is the HTTP method to update resource
* Which is the HTTP method to delete resource
* How to request Rest API

---
## Python Scripts

* Allowed editors: vi, vim, emacs
* All your files will be interpreted/compiled on Ubuntu 14.04 LTS using python3 (version 3.4.3)
* All your files should end with a new line
* The first line of all your files should be exactly #!/usr/bin/python3
* A README.md file, at the root of the folder of the project, is mandatory
* Your code should use the PEP 8 style (version 1.7.*)
* All your files must be executable
* The length of your files will be tested using wc
* All your modules should have documentation (python3 -c 'print(__import__("my_module").__doc__)')
* All your classes should have documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
* All your functions (inside and outside a class) should have documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')

---
## Python Unit Tests
* Allowed editors: vi, vim, emacs
* All your files should end with a new line
* All your test files should be inside a folder tests
* You have to use the unittest module
* All your test files should be python files (extension: .py)
* All your test files and folders should start by test_
* Your file organization in the tests folder should be the same as your project: ex: for models/base_model.py, unit tests must be in: tests/test_models/test_base_model.py
* All your tests should be executed by using this command: python3 -m unittest discover tests
* You can also test file by file by using this command: python3 -m unittest tests/test_models/test_base_model.py
* We strongly encourage you to work together on test cases, so that you don’t miss any edge cases

---
## Install Flask
```
$ pip3 install Flask
```

---
### [0. Restart from scratch!](https://github.com/alexaorrico/AirBnB_clone_v2)

No no no! We are already too far in the project to restart everything.

But once again, let’s work on a new codebase.

For this project you will fork this [codebase](https://github.com/alexaorrico/AirBnB_clone_v2)

* Update the repository name to AirBnB_clone_v3
* Update the README.md:
* Add yourself as an author of the project
* Add new information about your new contribution
* Make it better!
* If you’re the owner of this codebase, create a new repository called AirBnB_clone_v3 and copy over all files from AirBnB_clone_v2

### [1. Never fail!](./tests)
Since the beginning we’ve been using the unittest module, but do you know why unittests are so important? Because when you add a new feature, you refactor a piece of code, etc… you want to be sure you didn’t break anything.

At Holberton School, we have (as of 08/20/2018), 5213 unittests just for the intranet and they all pass!

The following requirements must be met for your project:
* all current tests must pass (don’t delete them…)
* add new tests as much as you can (tests are mandatory for some tasks)
```
guillaume@ubuntu:~/AirBnB_v3$ python3 -m unittest discover tests 2>&1 | tail -1
OK
guillaume@ubuntu:~/AirBnB_v3$ HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test HBNB_MYSQL_PWD=hbnb_test_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_test_db HBNB_TYPE_STORAGE=db python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1
OK
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [2. Code review]

Like “tests”, code review is the base of all software development.

All companies are using this “feature” to improve the codebase, but also the group dynamic. For example, at [Zenly](https://zen.ly/), the iOS team does a code review everyday at 5pm with the entire team.

What is a code review?

Code review helps developers learn the code base, as well as help them learn new technologies and techniques that grow their skill sets.

When a developer is finished working on an issue, another developer looks over the code and considers questions like:

* Are there any obvious logic errors in the code?
* Looking at the requirements, are all cases fully implemented?
* Are the new automated tests sufficient for the new code? Do existing automated tests need to be rewritten to account for changes in the code?
* Does the new code conform to existing style guidelines?

As references:

* [Why code reviews matter (and actually save time!)](https://www.atlassian.com/agile/software-development/code-reviews)
* [Code Review Best Practices](https://www.kevinlondon.com/2015/05/05/code-review-best-practices.html)
* [Github - code review tool](https://github.com/features#code-review)
* [Code Review on GitHub](https://www.youtube.com/watch?v=HW0RPaJqm4g)
* [Effective pull requests and other good practices for teams using Github](https://codeinthehole.com/tips/pull-requests-and-other-good-practices-for-teams-using-github/)
* [Merging vs. Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

For this project, you will need to review a peer’s pull request on the branch storage_get_count (which will be made for question 3), and then accept the pull request, with your review in the comments.

What we expect:
* a file code_review.txt, containing the Github username of the student you reviewed (ex: If you did the review of JohnDoe, code_review.txt must contain JohnDoe)
* The code review must be done on Github, in the comments for the pull request:
* the pull request must be created from the branch storage_get_count by a peer
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

### [3. Improve storage](./models)
Update DBStorage and FileStorage, adding two new methods. All changes should be done in the branch storage_get_count:

A method to retrieve one object:
* Prototype: def get(self, cls, id):
* cls: class name
* id: string representing the object ID
* Returns the object based on the class name and its ID, or None if not found

A method to count the number of objects in storage:
* Prototype: def count(self, cls=None):
* cls: class name (optional)
* Returns the number of objects in storage matching the given class name. If no name is passed, returns the count of all objects in storage.

Don’t forget to add new tests for these 2 methods on each storage engine.
```
guillaume@ubuntu:~/AirBnB_v3$ cat test_get_count.py
#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

guillaume@ubuntu:~/AirBnB_v3$
guillaume@ubuntu:~/AirBnB_v3$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./test_get_count.py 
All objects: 1013
State objects: 27
First state: [State] (f8d21261-3e79-4f5c-829a-99d7452cd73c) {'name': 'Colorado', 'updated_at': datetime.datetime(2017, 3, 25, 2, 17, 6), 'created_at': datetime.datetime(2017, 3, 25, 2, 17, 6), '_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fc0103a8e80>, 'id': 'f8d21261-3e79-4f5c-829a-99d7452cd73c'}
guillaume@ubuntu:~/AirBnB_v3$
guillaume@ubuntu:~/AirBnB_v3$ ./test_get_count.py 
All objects: 19
State objects: 5
First state: [State] (af14c85b-172f-4474-8a30-d4ec21f9795e) {'updated_at': datetime.datetime(2017, 4, 13, 17, 10, 22, 378824), 'name': 'Arizona', 'id': 'af14c85b-172f-4474-8a30-d4ec21f9795e', 'created_at': datetime.datetime(2017, 4, 13, 17, 10, 22, 378763)}
guillaume@ubuntu:~/AirBnB_v3$ 
```
For this task, you must make a pull request on Github.com, and ask at least one of your peer to review and merge it.

Please do not delete this branch, a manual review for grading will be done using this branch.

### [4. Status of your API](./api)

It’s time to start your API!

Your first endpoint (route) will be to return the status of your API:
```
guillaume@ubuntu:~/AirBnB_v3$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
...
```
In another terminal:
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/status
{
  "status": "OK"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET -s http://0.0.0.0:5000/api/v1/status -vvv 2>&1 | grep Content-Type
< Content-Type: application/json
guillaume@ubuntu:~/AirBnB_v3$ 
```
Magic right? (No need to have a pretty rendered output, it’s a JSON, only the structure is important)

Ok, let starts:

* Create a folder api at the root of the project with an empty file __init__.py
* Create a folder v1 inside api:
* create an empty file __init__.py
* create a file app.py:
* create a variable app, instance of Flask
* import storage from models
* import app_views from api.v1.views
* register the blueprint app_views to your Flask instance app
* declare a method to handle @app.teardown_appcontext that calls storage.close()
* inside if __name__ == "__main__":, run your Flask server (variable app) with:
* host = environment variable HBNB_API_HOST or 0.0.0.0 as default value
* port = environment variable HBNB_API_PORT or 5000 as default value
* threaded=True
* Create a folder views inside v1:
* create a file __init__.py:
* import Blueprint from flask doc
* create a variable app_views which is an instance of Blueprint (url prefix must be /api/v1)
* wildcard import of everything in the package api.v1.views.index => PEP8 will complain about it, don’t worry, it’s normal and this file (views/v1/__init__.py) won’t be check.
* create a file index.py
* import app_views from api.v1.views
* create a route /status on the object app_views that returns a JSON: "status": "OK" (see example)

### [5. Some stats?](./api/v1/views/index.py)
Create an endpoint that retrieves the number of each objects by type:
* In api/v1/views/index.py
* Route: /api/v1/stats
* You must use the newly added count() method from storage
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/stats
{
  "amenities": 47, 
  "cities": 36, 
  "places": 154, 
  "reviews": 718, 
  "states": 27, 
  "users": 31
}
guillaume@ubuntu:~/AirBnB_v3$ 
```
(No need to have a pretty rendered output, it’s a JSON, only the structure is important)

### [6. Not found]
Designers are really creative when they have to design a “404 page”, a “Not found”… [34 brilliantly designed 404 error pages](https://www.creativebloq.com/web-design/best-404-pages-812505)

Today it’s different, because you won’t use HTML and CSS, but JSON!

In api/v1/app.py, create a handler for 404 errors that returns a JSON-formatted 404 status code response. The content should be: "error": "Not found"
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/nop
{
  "error": "Not found"
}
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/nop -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/nop HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.51.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 404 NOT FOUND
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Fri, 14 Apr 2017 23:43:24 GMT
< 
{
  "error": "Not found"
}
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [7. State](
Create a new view for State objects that handles all default RestFul API actions:
* In the file api/v1/views/states.py
* You must use to_dict() to retrieve an object into a valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all State objects: GET /api/v1/states

Retrieves a State object: GET /api/v1/states/<state_id>
* If the state_id is not linked to any State object, raise a 404 error

Deletes a State object:: DELETE /api/v1/states/<state_id>
* If the state_id is not linked to any State object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a State: POST /api/v1/states
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
* Returns the new State with the status code 201

Updates a State object: PUT /api/v1/states/<state_id>
* If the state_id is not linked to any State object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
* Update the State object with all key-value pairs of the dictionary.
* Ignore keys: id, created_at and updated_at
* Returns the State object with the status code 200
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/
[
  {
    "__class__": "State", 
    "created_at": "2017-04-14T00:00:02", 
    "id": "8f165686-c98d-46d9-87d9-d6059ade2d99", 
    "name": "Louisiana", 
    "updated_at": "2017-04-14T00:00:02"
  }, 
  {
    "__class__": "State", 
    "created_at": "2017-04-14T16:21:42", 
    "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269", 
    "name": "Arizona", 
    "updated_at": "2017-04-14T16:21:42"
  }, 
...
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/8f165686-c98d-46d9-87d9-d6059ade2d99
 {
  "__class__": "State", 
  "created_at": "2017-04-14T00:00:02", 
  "id": "8f165686-c98d-46d9-87d9-d6059ade2d99", 
  "name": "Louisiana", 
  "updated_at": "2017-04-14T00:00:02"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X POST http://0.0.0.0:5000/api/v1/states/ -H "Content-Type: application/json" -d '{"name": "California"}' -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/states/ HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.51.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 22
> 
* upload completely sent off: 22 out of 22 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 195
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sat, 15 Apr 2017 01:30:27 GMT
< 
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:27.557877", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California", 
  "updated_at": "2017-04-15T01:30:27.558081"
}
* Curl_http_done: called premature == 0
* Closing connection 0
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X PUT http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6 -H "Content-Type: application/json" -d '{"name": "California is so cool"}'
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:28", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California is so cool", 
  "updated_at": "2017-04-15T01:51:08.044996"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
{
  "__class__": "State", 
  "created_at": "2017-04-15T01:30:28", 
  "id": "feadaa73-9e4b-4514-905b-8253f36b46f6", 
  "name": "California is so cool", 
  "updated_at": "2017-04-15T01:51:08"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X DELETE http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
{}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/feadaa73-9e4b-4514-905b-8253f36b46f6
{
  "error": "Not found"
}
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [8. City](./api/v1/views/cities.py)
Same as State, create a new view for City objects that handles all default Rest

Full API actions:
* In the file api/v1/views/cities.py
* You must use to_dict() to serialize an object into valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all City objects of a State: GET /api/v1/states/<state_id>/cities
* If the state_id is not linked to any State object, raise a 404 error

Retrieves a City object. : GET /api/v1/cities/<city_id>
* If the city_id is not linked to any City object, raise a 404 error

Deletes a City object: DELETE /api/v1/cities/<city_id>
* If the city_id is not linked to any City object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a City: POST /api/v1/states/<state_id>/cities
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the state_id is not linked to any State object, raise a 404 error
* If the HTTP body request is not a valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
* Returns the new City with the status code 201

Updates a City object: PUT /api/v1/cities/<city_id>
* If the city_id is not linked to any City object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* Update the City object with all key-value pairs of the dictionary
* Ignore keys: id, state_id, created_at and updated_at
* Returns the City object with the status code 200
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/not_an_id/cities/
{
  "error": "Not found"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/states/2b9a4627-8a9e-4f32-a752-9a84fa7f4efd/cities
[
  {
    "__class__": "City", 
    "created_at": "2017-03-25T02:17:06", 
    "id": "1da255c0-f023-4779-8134-2b1b40f87683", 
    "name": "New Orleans", 
    "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
    "updated_at": "2017-03-25T02:17:06"
  }, 
  {
    "__class__": "City", 
    "created_at": "2017-03-25T02:17:06", 
    "id": "45903748-fa39-4cd0-8a0b-c62bfe471702", 
    "name": "Lafayette", 
    "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
    "updated_at": "2017-03-25T02:17:06"
  }, 
  {
    "__class__": "City", 
    "created_at": "2017-03-25T02:17:06", 
    "id": "e4e40a6e-59ff-4b4f-ab72-d6d100201588", 
    "name": "Baton rouge", 
    "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
    "updated_at": "2017-03-25T02:17:06"
  }
]
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/cities/1da255c0-f023-4779-8134-2b1b40f87683
{
  "__class__": "City", 
  "created_at": "2017-03-25T02:17:06", 
  "id": "1da255c0-f023-4779-8134-2b1b40f87683", 
  "name": "New Orleans", 
  "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
  "updated_at": "2017-03-25T02:17:06"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X POST http://0.0.0.0:5000/api/v1/states/2b9a4627-8a9e-4f32-a752-9a84fa7f4efd/cities -H "Content-Type: application/json" -d '{"name": "Alexandria"}' -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> POST /api/v1/states/2b9a4627-8a9e-4f32-a752-9a84fa7f4efd/cities/ HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.51.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 22
> 
* upload completely sent off: 22 out of 22 bytes
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 249
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 16 Apr 2017 03:14:05 GMT
< 
{
  "__class__": "City", 
  "created_at": "2017-04-16T03:14:05.655490", 
  "id": "b75ae104-a8a3-475e-bf74-ab0a066ca2af", 
  "name": "Alexandria", 
  "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
  "updated_at": "2017-04-16T03:14:05.655748"
}
* Curl_http_done: called premature == 0
* Closing connection 0
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X PUT http://0.0.0.0:5000/api/v1/cities/b75ae104-a8a3-475e-bf74-ab0a066ca2af -H "Content-Type: application/json" -d '{"name": "Bossier City"}'
{
  "__class__": "City", 
  "created_at": "2017-04-16T03:14:06", 
  "id": "b75ae104-a8a3-475e-bf74-ab0a066ca2af", 
  "name": "Bossier City", 
  "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
  "updated_at": "2017-04-16T03:15:12.895894"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/cities/b75ae104-a8a3-475e-bf74-ab0a066ca2af
{
  "__class__": "City", 
  "created_at": "2017-04-16T03:14:06", 
  "id": "b75ae104-a8a3-475e-bf74-ab0a066ca2af", 
  "name": "Bossier City", 
  "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
  "updated_at": "2017-04-16T03:15:13"
}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X DELETE http://0.0.0.0:5000/api/v1/cities/b75ae104-a8a3-475e-bf74-ab0a066ca2af
{}
guillaume@ubuntu:~/AirBnB_v3$ 
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/cities/b75ae104-a8a3-475e-bf74-ab0a066ca2af
{
  "error": "Not found"
}
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [9. Amenity](api/v1/views/amenity.py)
Create a new view for Amenity objects that handles all default RestFul API actions:
* In the file api/v1/views/amenities.py
* You must use to_dict() to serialize an object into valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all Amenity objects: GET /api/v1/amenities

Retrieves a Amenity object: GET /api/v1/amenities/<amenity_id>
* If the amenity_id is not linked to any Amenity object, raise a 404 error

Deletes a Amenity object:: DELETE /api/v1/amenities/<amenity_id>
* If the amenity_id is not linked to any Amenity object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a Amenity: POST /api/v1/amenities
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
* Returns the new Amenity with the status code 201

Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
* If the amenity_id is not linked to any Amenity object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* Update the Amenity object with all key-value pairs of the dictionary
* Ignore keys: id, created_at and updated_at
* Returns the Amenity object with the status code 200


### [10. User](api/v1/views/user.py)
Create a new view for User object that handles all default RestFul API actions:
* In the file api/v1/views/users.py
* You must use to_dict() to retrieve an object into a valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all User objects: GET /api/v1/users

Retrieves a User object: GET /api/v1/users/<user_id>
* If the user_id is not linked to any User object, raise a 404 error

Deletes a User object:: DELETE /api/v1/users/<user_id>
* If the user_id is not linked to any User object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a User: POST /api/v1/users
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key email, raise a 400 error with the message Missing email
* If the dictionary doesn’t contain the key password, raise a 400 error with the message Missing password
* Returns the new User with the status code 201

Updates a User object: PUT /api/v1/users/<user_id>
* If the user_id is not linked to any User object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP body request to a dictionary
* If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
* Update the User object with all key-value pairs of the dictionary
* Ignore keys: id, email, created_at and updated_at
* Returns the User object with the status code 200


### [11. Place](api/v1/views/place.py)
Create a new view for Place objects that handles all default RestFul API actions:
* In the file api/v1/views/places.py
* You must use to_dict() to retrieve an object into a valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all Place objects of a City: GET /api/v1/cities/<city_id>/places
* If the city_id is not linked to any City object, raise a 404 error

Retrieves a Place object. : GET /api/v1/places/<place_id>
* If the place_id is not linked to any Place object, raise a 404 error

Deletes a Place object: DELETE /api/v1/places/<place_id>
* If the place_id is not linked to any Place object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a Place: POST /api/v1/cities/<city_id>/places
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the city_id is not linked to any City object, raise a 404 error
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
* If the user_id is not linked to any User object, raise a 404 error
* If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
* Returns the new Place with the status code 201

Updates a Place object: PUT /api/v1/places/<place_id>
* If the place_id is not linked to any Place object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* Update the Place object with all key-value pairs of the dictionary
* Ignore keys: id, user_id, city_id, created_at and updated_at
* Returns the Place object with the status code 200

### [12. Reviews](api/v1/views/reviews.py)
Create a new view for Review object that handles all default RestFul API actions:
* In the file api/v1/views/places_reviews.py
* You must use to_dict() to retrieve an object into valid JSON
* Update api/v1/views/__init__.py to import this new file

Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews
* If the place_id is not linked to any Place object, raise a 404 error

Retrieves a Review object. : GET /api/v1/reviews/<review_id>
* If the review_id is not linked to any Review object, raise a 404 error

Deletes a Review object: DELETE /api/v1/reviews/<review_id>
* If the review_id is not linked to any Review object, raise a 404 error
* Returns an empty dictionary with the status code 200

Creates a Review: POST /api/v1/places/<place_id>/reviews
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the place_id is not linked to any Place object, raise a 404 error
* If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
* If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
* If the user_id is not linked to any User object, raise a 404 error
* If the dictionary doesn’t contain the key text, raise a 400 error with the message Missing text
* Returns the new Review with the status code 201

Updates a Review object: PUT /api/v1/reviews/<review_id>
* If the review_id is not linked to any Review object, raise a 404 error
* You must use request.get_json from Flask to transform the HTTP request to a dictionary
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* Update the Review object with all key-value pairs of the dictionary
* Ignore keys: id, user_id, place_id, created_at and updated_at
* Returns the Review object with the status code 200


### [13. HTTP access control (CORS)](./api/v1/app.py)
A resource makes a cross-origin HTTP request when it requests a resource from a different domain, or port, than the one the first resource itself serves.

Read the full definition here

Why do we need this?

Because you will soon start allowing a web client to make requests your API. If your API doesn’t have a correct CORS setup, your web client won’t be able to access your data.

With Flask, it’s really easy, you will use the class CORS of the module flask_cors.

How to install it: $ pip3 install flask_cors

Update api/v1/app.py to create a CORS instance allowing: /* for 0.0.0.0

You will update it later when you will deploy your API to production.

Now you can see this HTTP Response Header: < Access-Control-Allow-Origin: 0.0.0.0
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X GET http://0.0.0.0:5000/api/v1/cities/1da255c0-f023-4779-8134-2b1b40f87683 -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/states/2b9a4627-8a9e-4f32-a752-9a84fa7f4efd/cities/1da255c0-f023-4779-8134-2b1b40f87683 HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.51.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Access-Control-Allow-Origin: 0.0.0.0
< Content-Length: 236
< Server: Werkzeug/0.12.1 Python/3.4.3
< Date: Sun, 16 Apr 2017 04:20:13 GMT
< 
{
  "__class__": "City", 
  "created_at": "2017-03-25T02:17:06", 
  "id": "1da255c0-f023-4779-8134-2b1b40f87683", 
  "name": "New Orleans", 
  "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", 
  "updated_at": "2017-03-25T02:17:06"
}
* Curl_http_done: called premature == 0
* Closing connection 0
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [14. Place - Amenity](./api/v1/views/places_amenities.py)
Create a new view for the link between Place objects and Amenity objects that handles all default RestFul API actions:
* In the file api/v1/views/places_amenities.py
* You must use to_dict() to retrieve an object into a valid JSON
* Update api/v1/views/__init__.py to import this new file
* Depending of the storage:
* DBStorage: list, create and delete Amenity objects from amenities relationship
* FileStorage: list, add and remove Amenity ID in the list amenity_ids of a Place object

Retrieves the list of all Amenity objects of a Place: GET /api/v1/places/<place_id>/amenities

* If the place_id is not linked to any Place object, raise a 404 error

Deletes a Amenity object to a Place: DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
* If the place_id is not linked to any Place object, raise a 404 error
* If the amenity_id is not linked to any Amenity object, raise a 404 error
* If the Amenity is not linked to the Place before the request, raise a 404 error
* Returns an empty dictionary with the status code 200

Link a Amenity object to a Place: POST /api/v1/places/<place_id>/amenities/<amenity_id>
* No HTTP body needed
* If the place_id is not linked to any Place object, raise a 404 error
* If the amenity_id is not linked to any Amenity object, raise a 404 error
* If the Amenity is already linked to the Place, return the Amenity with the status code 200
* Returns the Amenity with the status code 201

### [15. Security improvements!](./models/base_model.py)
Currently, the User object is designed to store the user password in cleartext.

It’s super bad!
To avoid that, improve the User object:
* Update the method to_dict() of BaseModel to remove the password key except when it’s used by FileStorage to save data to disk. Tips: default parameters
* Each time a new User object is created or password updated, the password is hashed to a [MD5](https://docs.python.org/3.4/library/hashlib.html) value
* In the database for DBStorage, the password stored is now hashed to a MD5 value
* In the file for FileStorage, the password stored is now hashed to a MD5 value


### [16. Search](./api/v1/views/places.py)
For the moment, the only way to list Place objects is via GET /api/v1/cities/<city_id>/places.

Good, but not enough…

Update api/v1/views/places.py to add a new endpoint: POST /api/v1/places_search that retrieves all Place objects depending of the JSON in the body of the request.

The JSON can contain 3 optional keys:
* states: list of State ids
* cities: list of City ids
* amenities: list of Amenity ids

Search rules:
* If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
* If the JSON body is empty or each list of all keys are empty: retrieve all Place objects
* If states list is not empty, search for Place objects inside each State ids listed
* If cities list is not empty, search for Place objects inside each City ids listed
* states and cities are inclusive. Result will be Place from all cities and all City linked to all states
* If amenities list is not empty, search for Place objects having all Amenity ids listed
* amenities are exclusive. Result will be only Place having all amenities. If a Place doesn’t have one of these amenities, it won’t be retrieved.
```
guillaume@ubuntu:~/AirBnB_v3$ curl -X POST http://0.0.0.0:5000/api/v1/places_search -H "Content-Type: application/json" -d '{"states": ["2b9a4627-8a9e-4f32-a752-9a84fa7f4efd", "459e021a-e794-447d-9dd2-e03b7963f7d2"], "cities": ["5976f0e7-5c5f-4949-aae0-90d68fd239c0"]}'
[
  {
    "__class__": "Place", 
    "created_at": "2017-03-25T02:17:06", 
    "id": "dacec983-cec4-4f68-bd7f-af9068a305f5", 
    "name": "The Lynn House", 
    "city_id": "1721b75c-e0b2-46ae-8dd2-f86b62fb46e6, 
    "user_id": "3ea61b06-e22a-459b-bb96-d900fb8f843a", 
    "description": "Our place is 2 blocks from Vista Park (Farmer's Market), Historic Warren Ballpark, and about 2 miles from Old Bisbee where there is shopping, dining, and site seeing. We offer continental breakfast. You get the quiet life with great mountain and garden views. This is a 100+ year old cozy home which has been on both the Garden and Home tours. You have access to whole house, except for 1 restricted area (She-Shack).  Hosts are on site in a casita in the back from 8pm until 7am when we are in town.<BR /><BR />Our home has two bedrooms, one king and one queen.  There are 2 bathrooms, 1  1950's soak tub with shower and 1 with shower only.  Guests have access to the living/dining room area, and the kitchen (except for use of stove/oven).  Each morning, coffee/tea, and muffins are ready for guests.  A small frig is available in the dining room with water/juice and an area for guest items.  1 parking space is directly across the street.", 
    "number_rooms": 2,
    "number_bathrooms": 2,
    "max_guest": 4,
    "price_by_night": 82, 
    "latitude": 31.4141, 
    "longitude": -109.879, 
    "updated_at": "2017-03-25T02:17:06"
  },
...
guillaume@ubuntu:~/AirBnB_v3$ 
```

### [17. Documentation](
Nothing better than writing tests… and documentation!

But with [Swagger](https://swagger.io/), it’s really easy!

You will use the Flask version of Swagger: [Flasgger](https://github.com/flasgger/flasgger)

How to install it: $ pip3 install flasgger

Add comments on each endpoint of your API, so you can view the documentation in your browser: http://0.0.0.0:5000/apidocs

It is your responsibility to request a review for this task from a peer before the project’s deadline. If no peers have been reviewed, you should request a review from a TA or staff member.

---
## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)
Robinson Montes - [Github](https://github.com/mecomonteshbtn) / [Twitter](https://twitter.com/mecomontes)
Mauricio Olarte - [Github](https://github.com/mauricioolarte) / [Twitter](https://twitter.com/reneolarte)

Second part of Airbnb: Joann Vuong
## License
Public Domain. No copy write protection. 
