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
* `def delete(self)` - delete the current instance from the storage

Classes inherited from Base Model:
* [amenity.py](/models/amenity.py)
* [city.py](/models/city.py)
* [place.py](/models/place.py)
* [review.py](/models/review.py)
* [state.py](/models/state.py)
* [user.py](/models/user.py)

#### `/models/engine` directory contains File Storage class that handles JASON serialization and deserialization and DBStorage for MySQL database :
[file_storage.py](/models/engine/file_storage.py) - serializes instances to a JSON file & deserializes back to instances
* `def all(self)` - returns the dictionary __objects
* `def new(self, obj)` - sets in __objects the obj with key <obj class name>.id
* `def save(self)` - serializes __objects to the JSON file (path: __file_path)
* `def reload(self)` -  deserializes the JSON file to __objects
* `def delete(self, obj=None)` - delete obj from __objects if it’s inside
* `def close(self)` - call reload() method for deserializing the JSON file to objects
* `def get(self, cls, id)` - return the specific object based on the class and its ID, or None if not found
* `def count(self, cls=None)` - count number of objects in DB storage (if no class : all object storage, if class : all object of specific class)

[db_storage.py](/models/engine/db_storage.py) - storage in MySQL database
* `def all(self, cls=None)` - query on the current database session
* `def new(self, obj)` - add the object to the current database session
* `def save(self)` - commit all changes of the current database session
* `def delete(self, obj=None)` - delete from the current database session obj if not None
* `def reload(self)` - reloads data from the database
* `def close(self)` - call remove() method on the private session attribute
* `def get(self, cls, id)` - return the specific object based on the class and its ID, or None if not found
* `def count(self, cls=None)` - count number of objects in DB storage (if no class : all object storage, if class : all object of specific class)

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
* `def test_instantiation(self)` - Test that object is correctly created
* `def test_datetime_attributes(self)` - Test that two BaseModel instances have different datetime objects and that upon creation have identical updated_at and created_at value
* `def test_uuid(self)` - Test that id is a valid uuid
* `def test_to_dict(self)` - Test conversion of object attributes to dictionary for json
* `def test_to_dict_values(self)` - test that values in dict returned from to_dict are correct
* `def test_str(self)` - test that the str method has the correct output
* `def test_save(self, mock_storage)` - Test that save method updates `updated_at` and calls `storage.save`

[/test_models/test_amenity.py](/tests/test_models/test_amenity.py) - Contains the TestAmenityDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_amenity(self)` - Test that models/amenity.py conforms to PEP8
* `def test_pep8_conformance_test_amenity(self)` - Test that tests/test_models/test_amenity.py conforms to PEP8
* `def test_amenity_module_docstring(self)` - Test for the amenity.py module docstring
* `def test_amenity_class_docstring(self)` - Test for the Amenity class docstring
* `def test_amenity_func_docstrings(self)` - Test for the presence of docstrings in Amenity methods

Contains the TestAmenity class:
* `def test_is_subclass(self)` - Test that Amenity is a subclass of BaseModel
* `def test_name_attr(self)` - Test that Amenity has attribute name, and it's as an empty string
* `def test_to_dict_creates_dict(self)`- test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - test that values in dict returned from to_dict are correct
* `def test_str(self)` - test that the str method has the correct output


[/test_models/test_city.py](/tests/test_models/test_city.py) - Contains the TestCityDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_city(self)` - Test that models/city.py conforms to PEP8
* `def test_pep8_conformance_test_city(self)` - Test that tests/test_models/test_city.py conforms to PEP8
* `def test_city_module_docstring(self)` - Test for the city.py module docstring
* `def test_city_class_docstring(self)` - Test for the City class docstring
*  `def test_city_func_docstrings(self)` - Test for the presence of docstrings in City methods

Contains the TestCity class:
* `def test_is_subclass(self)` - Test that City is a subclass of BaseModel
* `def test_name_attr(self)`- Test that City has attribute name, and it's an empty string
* `def test_state_id_attr(self)` - Test that City has attribute state_id, and it's an empty string
* `def test_to_dict_creates_dict(self)` - test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - test that values in dict returned from to_dict are correct
* `def test_str(self)` - test that the str method has the correct output

[/test_models/test_file_storage.py](/tests/test_models/test_file_storage.py) - Contains the TestFileStorageDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_file_storage(self)` - Test that models/file_storage.py conforms to PEP8
* `def test_pep8_conformance_test_file_storage(self)` - Test that tests/test_models/test_file_storage.py conforms to PEP8
* `def test_file_storage_module_docstring(self)` - Test for the file_storage.py module docstring
* `def test_file_storage_class_docstring(self)` - Test for the FileStorage class docstring
* `def test_fs_func_docstrings(self)` - Test for the presence of docstrings in FileStorage methods

Contains the TestFileStorage class:
* `def test_all_returns_dict(self)` - Test that all returns the FileStorage.__objects attr
* `def test_new(self)` - Test that new adds an object to the FileStorage.__objects attr
* `def test_save(self)` - Test that save properly saves objects to file.json
* `def test_get(self)`- Test that get properly objects valid class and id
* `def test_get_bad_id(self)` - Test that get properly objects invalid id
* `def test_get_bad_id(self)`- Test that get properly objects invalid class
* `def test_count(self)` - Test all count for class city
* `def test_count_all(self)` - Test all count
* `def test_count_class(self)`- Test all count for class city

[/test_models/test_db_storage.py](/tests/test_models/test_db_storage.py) - Contains the TestDBStorageDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_db_storage` - Test that models/engine/db_storage.py conforms to PEP8
* `def test_pep8_conformance_test_db_storage(self)` - Test tests/test_models/test_db_storage.py conforms to PEP8
* `def test_db_storage_module_docstring(self)` - Test for the db_storage.py module docstring
* `def test_db_storage_class_docstring(self)` - Test for the DBStorage class docstring
* `def test_dbs_func_docstrings(self)` - Test for the presence of docstrings in DBStorage methods

Contains the TestDBStorage class:
* `def test_all_returns_dict(self)` - Test that all returns a dictionaty
* `def test_all_no_class(self)` - Test that all returns all rows when no class is passed
* `def test_new(self)` - test that new adds an object to the database
* `def test_save(self)` - Test that save properly saves objects to file.json
* `def test_get(self)` - Test that get returns an object base on its id
* `def test_count(self)` - Test that count return the number of objects


[/test_models/test_place.py](/tests/test_models/test_place.py) - Contains the TestPlaceDoc class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_place(self)` - Test that models/place.py conforms to PEP8.
* `def test_pep8_conformance_test_place(self)` - Test that tests/test_models/test_place.py conforms to PEP8.
* `def test_place_module_docstring(self)` - Test for the place.py module docstring
* `def test_place_class_docstring(self)` - Test for the Place class docstring
* `def test_place_func_docstrings(self)` - Test for the presence of docstrings in Place methods

Contains the TestPlace class:
* `def test_is_subclass(self)` - Test that Place is a subclass of BaseModel
* `def test_city_id_attr(self)` - Test Place has attr city_id, and it's an empty string
* `def test_user_id_attr(self)` - Test Place has attr user_id, and it's an empty string
* `def test_name_attr(self)` - Test Place has attr name, and it's an empty string
* `def test_description_attr(self)` - Test Place has attr description, and it's an empty string
* `def test_number_rooms_attr(self)` - Test Place has attr number_rooms, and it's an int == 0
* `def test_number_bathrooms_attr(self)` - Test Place has attr number_bathrooms, and it's an int == 0
* `def test_max_guest_attr(self)` - Test Place has attr max_guest, and it's an int == 0
* `def test_price_by_night_attr(self)` - Test Place has attr price_by_night, and it's an int == 0
* `def test_latitude_attr(self)` - Test Place has attr latitude, and it's a float == 0.0
* `def test_longitude_attr(self)` - Test Place has attr longitude, and it's a float == 0.0
* `def test_amenity_ids_attr(self)` - Test Place has attr amenity_ids, and it's an empty list
* `def test_to_dict_creates_dict(self)` - test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - test that values in dict returned from to_dict are correct
* `def test_str(self)` - test that the str method has the correct output

[/test_models/test_review.py](/tests/test_models/test_review.py) - Contains the TestReviewDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_review(self)` - Test that models/review.py conforms to PEP8
* `def test_pep8_conformance_test_review(self)` - Test that tests/test_models/test_review.py conforms to PEP8
* `def test_review_module_docstring(self)` - Test for the review.py module docstring
* `def test_review_class_docstring(self)` - Test for the Review class docstring
* `def test_review_func_docstrings(self)` - Test for the presence of docstrings in Review methods

Contains the TestReview class:
* `def test_is_subclass(self)` - Test if Review is a subclass of BaseModel
* `def test_place_id_attr(self)` - Test Review has attr place_id, and it's an empty string
* `def test_user_id_attr(self)` - Test Review has attr user_id, and it's an empty string
* `def test_text_attr(self)` - Test Review has attr text, and it's an empty string
* `def test_to_dict_creates_dict(self)` - test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - Test that values in dict returned from to_dict are correct
* `def test_str(self)` - Test that the str method has the correct output

[/test_models/state.py](/tests/test_models/test_state.py) - Contains the TestStateDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_state(self)` - Test that models/state.py conforms to PEP8
* `def test_pep8_conformance_test_state(self)` - Test that tests/test_models/test_state.py conforms to PEP8
* `def test_state_module_docstring(self)` - Test for the state.py module docstring
* `def test_state_class_docstring(self)` - Test for the State class docstring
* `def test_state_func_docstrings(self)` - Test for the presence of docstrings in State methods

Contains the TestState class:
* `def test_is_subclass(self)` - Test that State has attribute name, and it's as an empty string
* `def test_to_dict_creates_dict(self)` - Test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - Test that values in dict returned from to_dict are correct
* `def test_str(self)` - Test that the str method has the correct output

[/test_models/user.py](/tests/test_models/test_user.py) - Contains the TestUserDocs class:
* `def setUpClass(cls)` - Set up for the doc tests
* `def test_pep8_conformance_user(self)` - Test that models/user.py conforms to PEP8
* `def test_pep8_conformance_test_user(self)` - Test that tests/test_models/test_user.py conforms to PEP8
* `def test_user_module_docstring(self)` - Test for the user.py module docstring
* `def test_user_class_docstring(self)` - Test for the User class docstring
* `def test_user_func_docstrings(self)` - Test for the presence of docstrings in User methods

Contains the TestUser class:
* `def test_is_subclass(self)` - Test that User is a subclass of BaseModel
* `def test_email_attr(self)` - Test that User has attr email, and it's an empty string
* `def test_password_attr(self)` - Test that User has attr password, and it's an empty string
* `def test_first_name_attr(self)` - Test that User has attr first_name, and it's an empty string
* `def test_last_name_attr(self)` - Test that User has attr last_name, and it's an empty string
* `def test_to_dict_creates_dict(self)` - test to_dict method creates a dictionary with proper attrs
* `def test_to_dict_values(self)` - test that values in dict returned from to_dict are correct
* `def test_str(self)` - test that the str method has the correct output


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


#### AirBnB clone - RESTful API: a RESTful API has been implemented allowing access to the database 
Sonia Nguyen [Github](https://github.com/soniangn)  
Marianne Arrué [Github](https://github.com/MarianneHolbie)

## License
Public Domain. No copy write protection. 
