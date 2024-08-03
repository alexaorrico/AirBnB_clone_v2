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
* [Commands](#commands)
* [File Descriptions](#file-descriptions)
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

## Commands
| Command     |  Description                                                                                     | Usage                                          |
| :---------- | :----------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| `EOF`       | exits console                                                                                    | `EOF`                                          |
| `quit`      | exits console                                                                                    | `quite`                                        |
| `create`    | creates a new object, saves it to storage and prints the id                                      | `create <ClassName>`                           |
| `destroy`   | deletes an object from storage                                                                   | `destroy <ClassName> <ObjectID>`               |
| `show`      | prints the string representation of an object                                                    | `show <ClassName> <ObjectID>`                  |
| `all`       | prints the string representation of all objects or all instances of a specified class in storage | `all` or `all <ClassName>`                     |
| `update`    | update an existing object (to add or change the value of an attribute but not to remove)         | `update <ClassName> <ObjectID> <attr> <value>` |

In addition to the command format above, the following also exist:
| Command     |  Description                                                                                   | Usage                                                       |
| :---------- | :--------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `all`       | prints the string representation of all instances of a specified class in storage              | `<ClassName>.all()`                                         |
| `count`     | retrieves the number of instances of a specified class                                         | `<ClassName>.count()`                                       |
| `destroy`   | deletes an object from storage                                                                 | `<ClassName>.destory(<ObjectID>)`                           |
| `show`      | prints the string representation of an object                                                  | `<ClassName>.show(<ObjectID>)`                              |
| `update`    | update an existing object (to add or change the value of an attribute but not to remove)       | `<ClassName>.update(<ObjectID>, <attr>, <value>)...`        |
| `update`    | update an existing object with a dictionary representation of attributes and values            | `<ClassName>.update(<ObjectID>, {"<attr>": "<value>"},...)` |

## File Descriptions
[console.py](console.py) - the console contains the entry point of the command interpreter. 

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

#### `/models/engine` directory contains File Storage class that handles JASON serialization and deserialization  and the DB_storage class that handles the saving of data in a persistent RDB storage (A MySQL Database):
[file_storage.py](/models/engine/file_storage.py) - serializes instances to a JSON file & deserializes back to instances  
Class defined here:  
*`class FileStorage`  
Methods defined here:  
&emsp; * `def all(self)` - returns the dictionary __objects  
&emsp; * `def new(self, obj)` - sets in __objects the obj with key <obj class name>.id  
&emsp; * `def save(self)` - serializes __objects to the JSON file (path: __file_path)  
&emsp; * ` def reload(self)` -  deserializes the JSON file to __objects  
&emsp; * `def delete(self, obj=None)` - delete object `obj` from __objects if it’s inside  
&emsp; * `def close(self)` - call the reload(self) method  

[db_storage.py](/models/engine/db_storage.py) - uses object relational mapper to interact with MySQL database to create, modify and store data in RDB  
Class defined here  
*`class DBStorage`  
Methods defined here:  
&emsp; * `def all(self, cls=None)` - query on the database to return all objects or the specified object by the argument `cls`  
&emsp; * `def new(self, obj)` - adds a new object to the current database session  
&emsp; * `def save(self)` - commits and save all changes of the current database session  
&emsp; * `def reload(self)` -  loads data from database into runtime  
&emsp; * `def delete(self, obj=None)` - delete an object `obj` from the current database session  
&emsp; * `def close(self)` - closes current database session and release all existing transaction  

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
(hbnb) City.show(acc962fd-a154-45ed-9acd-423eae5a2bbf)
[City] (acc962fd-a154-45ed-9acd-423eae5a2bbf) {'id': 'acc962fd-a154-45ed-9acd-423eae5a2bbf', 'created_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 35678), 'updated_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 35886), 'state_id': '06fdb9f6-b5fe-4eaf-a77f-279623ce1b7b', 'name': 'Fremont'}
(hbnb) quit
(hbnb) City.all()
["[City] (acc962fd-a154-45ed-9acd-423eae5a2bbf) {'id': 'acc962fd-a154-45ed-9acd-423eae5a2bbf', 'created_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 35678), 'updated_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 35886), 'state_id': '06fdb9f6-b5fe-4eaf-a77f-279623ce1b7b', 'name': 'Fremont'}", "[City] (585e21cb-3dd5-47fe-849e-597ebc18eb7c) {'id': '585e21cb-3dd5-47fe-849e-597ebc18eb7c', 'created_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 36727), 'updated_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 36942), 'state_id': '06fdb9f6-b5fe-4eaf-a77f-279623ce1b7b', 'name': 'Napa'}", "[City] (646c81fa-8e73-436e-87ae-c200de6f411d) {'id': '646c81fa-8e73-436e-87ae-c200de6f411d', 'created_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 55817), 'updated_at': datetime.datetime(2024, 7, 29, 6, 45, 1, 56105), 'state_id': 'e226e9d7-c48a-41b6-b555-dcaca1fdd8ed', 'name': 'Sonoma'}", "[City] (12c6f011-dae5-401c-9c53-82cb8e715ed4) {'id': '12c6f011-dae5-401c-9c53-82cb8e715ed4', 'created_at': datetime.datetime(2024, 8, 2, 8, 44, 12, 143427), 'updated_at': datetime.datetime(2024, 8, 2, 8, 44, 12, 143487)}"]
```

## Bugs
No known bugs at this time. 

## Authors
Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)

Second part of Airbnb: Joann Vuong
Third version: Enyone Christian Achobe [Github](https://github.com/AEnyChris) / [Twitter](https://x.com/enyonejoseph)
## License
Public Domain. No copy write protection. 
