<img src="hbnb.png" alt="AirBnB Clone" height="100%" >

# AirBnB Clone v3

This is the third version of the AirBnB clone project. After the first two versions that focused on creating a command line interface and a web server, we are now adding a RESTful API to the project. This API will allow us to interact with the data in the database. We will be able to create, update, delete, and view data in the database. We will also be able to view data in the database in different formats, such as JSON.

<img src="https://camo.githubusercontent.com/d16c33f5026cf57b58cfce12282bf28a5b9efad867e7d4eed507e3a3fac3bdbc/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f696e7472616e65742d70726f6a656374732d66696c65732f636f6e63657074732f37342f68626e625f73746570342e706e67" alt="AirBnB Clone" height="100%" >

## Table of Content
* [Environment](#environment)
* [Installation](#installation)
* [AirBnB Clone - RESTful API](#airbnb-clone---restful-api)
* [AirBnB Clone - The Console](#airbnb-clone---the-console)
* [Examples of use](#examples-of-use)
* [Bug](#bugs)
* [Authors](#authors)
* [License](#license)


## Environment
This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)

**Environment variables:**
* `HBNB_ENV` - running environment. It can be `dev | test` for the moment.
* `HBNB_MYSQL_USER` - the username of your MySQL user.
* `HBNB_MYSQL_PWD` - the password of your MySQL user.
* `HBNB_MYSQL_HOST` - the hostname of your MySQL server (`localhost` by default).
* `HBNB_MYSQL_DB` - the name of your MySQL database.
* `HBNB_TYPE_STORAGE` - the type of storage used. It can be `file` (using `FileStorage`) or `db` (using `DBStorage`).
* `HBNB_API_PORT` - the port number of the API. It is `5000` by default.
* `HBNB_API_HOST` - the host of the API (`localhost` by default).



## Installation

* Clone this repository: `https://github.com/gichobih/AirBnB_clone_v3.git`
* Access AirBnb directory: `cd AirBnB_clone_v3`
* Run hbnb(interactively): `./console.py` and enter command
* Run hbnb(non-interactively): `echo "<command>" | ./console.py`
* Run API: `./api/v1/app.py` the API will be available at `http://localhost:5000/`

# AirBnB Clone - RESTful API

The RESTful API is the objective of this repository. The API will allow us to interact with the data in the database using CRUD operations (Create, Read, Update, Delete).

#### Functionalities of this RESTful API:
* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database etc...
* Do operations on objects (count, compute stats, etc...)
* Update attributes of an object
* Destroy an object
* Retrieve all objects of a class
* Retrieve an object by its ID
* Update an object


## File Descriptions

#### `/api/v1` directory contains the API:
[/api/v1/app.py](/api/v1/app.py) - Contains the Flask application that handles the API routes and error handling

#### `/api/v1/views` directory contains the views for the API:
[/api/v1/views/index.py](/api/v1/views/index.py) - Contains the index view that returns a JSON representation of the API status
* `def status()` - Returns a JSON representation of the API status

[/api/v1/views/states.py](/api/v1/views/states.py) - Contains the views for State objects that handles all default RestFul API actions
* `def get_states()` - Retrieves the list of all State objects
* `def get_state(state_id)` - Retrieves a State object
* `def delete_state(state_id)` - Deletes a State object
* `def create_state()` - Creates a State object
* `def update_state(state_id)` - Updates a State object

[/api/v1/views/cities.py](/api/v1/views/cities.py) - Contains the views for City objects that handles all default RestFul API actions
* `def get_cities(state_id)` - Retrieves the list of all City objects of a State
* `def get_city(city_id)` - Retrieves a City object
* `def delete_city(city_id)` - Deletes a City object
* `def create_city(state_id)` - Creates a City object
* `def update_city(city_id)` - Updates a City object



# AirBnB Clone - The Console

The console was the first segment of the AirBnB project at Holberton School that has collectively cover fundamental concepts of higher level programming.

#### Functionalities of this command interpreter:
* Create a new object (ex: a new User or a new Place)
* Retrieve an object from a file, a database etc...
* Do operations on objects (count, compute stats, etc...)
* Update attributes of an object
* Destroy an object


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

### AirBnB Console
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

### AirBnB API
```
user@host: cd AirBnB_clone_v3
user@host: python3 -m api.v1.app
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000
Press CTRL+C to quit
```

in another terminal:
```
user@host: curl -X GET http://0.0.0.0:5000/api/v1/status
{
  "status": "OK"
}
```


## Bugs
No known bugs at this time. 

## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)  
Dennis Murimi - [Github](https://github.com/gichobih)  
Ahmed Amine Nouabi - [Github](https://github.com/amineNouabi)  


Second part of Airbnb: Joann Vuong
## License
Public Domain. No copy write protection. 
