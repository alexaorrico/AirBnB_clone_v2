# AirBnB Clone - The Console
The console is the first segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level programming. In the third part, we add the definition of the application and its views, which contains the endpoints for the web app. The goal of AirBnB project is to eventually deploy our server a simple copy of the AirBnB Website(HBnB). A command interpreter is created in this segment to manage objects for the AirBnB(HBnB) website.

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

### `models/` directory contains classes used for this project:
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
* `def reload(self)` -  deserializes the JSON file to __objects

### `/api` directory contains the definition of the application and its views.
[/v1/app.py](/api/v1/app.py) - Contains the definition of the application and environment variables (port and host). Also, there are methods of errors handler and clase the session.
* `def not_found(error)`- Handler for 404 errors that returns a JSON 404 status code
* `def close_session(db)`- Allow close the session

[/v1/views/index.py](/api/v1/views/index.py) - Contains the index for the application.
* `def Index()`- Return a status code OK with the HTTP method GET.
* `def number_objects()`- Counts the number of objects for each class.

[/v1/views/amenities.py](/api/v1/views/amenities.py) - Contains the view for the Amenity class.
* `def all_amenities()`- Return a list of all objects of Amenity class.
* `def get_amenities(amenity_id)`- Return an amenity object according class and id of Amenity or return Error: Not found if it doesn't exist.
* `def delete_amenity(amenity_id)`- Deletes an object Amenity if exists, otherwise raise 404 error.
* `def response_amenity()`- Post request that allow to create a new amenity if exists the name or raise Error if is not a valid json or if the name is missing.
* `def update_amenity(amenity_id)`- Updates attributes from an Amenity object.

[/v1/views/cities.py](/api/v1/views/cities.py) - Contains the view for the City class.
* `def get_cities(state_id)`- Return cities according to id of state object or return error: Not found if it doesn't exist.
* `def get_city(city_id)`- Return a city object according class and id of City or return Error: Not found if it doesn't exist.
* `def delete_city(city_id)`- Deletes an object City if exists, otherwise raise 404 error.
* `def response_city(state_id)`- Post request that allow to create a new city if exists the State id or raise Error if is not a valid json or if the name is missing.
* `def update_city(city_id)`- Updates attributes from a City object.

[/v1/views/places.py](/api/v1/views/places.py) - Contains the view for the Place class.
* `def get_places(city_id)`- Return places according to id of city object or return error: Not found if it doesn't exist.
* `def get_place(place_id)`- Return a place object according class and id of Place or return Error: Not found if it doesn't exist.
* `def delete_place(place_id)`- Deletes a place object if exists, otherwise raise 404 error.
* `def response_place(city_id)`- Post request that allow to create a new place if exists the City id or raise Error if is not a valid json or if the name is missing.
* `def update_place(place_id)`- Updates attributes from a place object.

[/v1/views/places_reviews.py](/api/v1/views/places_reviews.py) - Contains the view for the Review class.
* `def get_reviews(place_id)`- Return reviews according to id of place object or return error: Not found if it doesn't exist.
* `def get_review(review_id)`- Return a review object according class and id of Review or return error: Not found if it doesn't exist.
* `def delete_review(review_id)`- Deletes a review object if exists, otherwise raise 404 error.
* `def response_reviews(place_id)`- Post request that allow to create a new review if exists the Place id or raise Error if is not a valid json or if the name is missing.
* `def update_review(review_id)`- Updates attributes from a review object.

[/v1/views/states.py](/api/v1/views/states.py) - Contains the view for the State class.
* `def all_states()`- Return a list of all objects of State class.
* `def get_states(state_id)`- Return a state object according class and id of State or return Error: Not found if it doesn't exist.
* `def delete_state(state_id)`- Deletes an object State if exists, otherwise raise 404 error.
* `def response_state()`- Post request that allow to create a new State if exists the name or raise Error if is not a valid json or if the name is missing.
* `def update_state(state_id)`- Updates attributes from a state object.

[/v1/views/users.py](/api/v1/views/users.py) - Contains the view for the User class.
* `def all_users()`- Return a list of all objects of User class.
* `def get_users(user_id)`- Return a user object according class and id of User or return Error: Not found if it doesn't exist.
* `def delete_user(user_id)`- Deletes an user object if exists, otherwise raise 404 error.
* `def response_user()`- Post request that allow to create a new User if exists the email and password or raise Error if is not a valid json or if the email and password is missing.
* `def update_user(user_id)`- Updates attributes from a user object.

### `/tests` directory contains all unit test cases for this project:
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
* `def test_fs_func_docstrings(self)` - Test for the presence of docstrings in FileStorage methods.
* `def test_all_returns_dict(self)` - Test that all returns the FileStorage.__objects attr
* `def test_new(self)` - Test that new adds an object to the FileStorage.__objects attr
* `def test_save(self)` - Test that save properly saves objects to file.json
* `def test_reload(self)` - Test that check the method reload
* `def test_count(self)` - Test that check the method count
* `def test_get(self)` - Test that check the method get

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

## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)

Second part of Airbnb: Joann Vuong

Third part of Airbnb:
Diego Gómez - [Twitter](https://twitter.com/dagomez2530)
Kimberly Hinostroza - [Twitter](https://twitter.com/H1030Kimberly)

## License
Public Domain. No copy write protection. 
