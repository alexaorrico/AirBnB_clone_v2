<h1>AirBnB Clone - The Console</h1>
<p>The console is the first segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level programming. The goal of AirBnB project is to eventually deploy our server a simple copy of the AirBnB Website(HBnB). A command interpreter is created in this segment to manage objects for the AirBnB(HBnB) website.</p>

<h4>Functionalities of this command interpreter:</h4>
<ul>
<li>Create a new object (ex: a new User or a new Place)</li>
<li> Retrieve an object from a file, a database etc...</li>
<li> Do operations on objects (count, compute stats, etc...)</li>
<li> Update attributes of an object</li>
<li> Destroy an object</li>
</ul>

<h2>Table of Content</h2>
<ul>
<li>Environment</li>
<li>Installation</li>
<li>File Descriptions</li>
<li>Usage</li>
<li>Examples of use</li>
<li>Bugs</li>
<li>Authors</li>
<li>License</li>
</ul>

<h2>Environment</h2>
<p>This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)</p>

<h2>Installation</h2>
<ul>
<li>Clone this repository: git clone "https://github.com/alexaorrico/AirBnB_clone.git"</li>
<li>Access AirBnb directory: cd AirBnB_clone</li>
<li>Run hbnb(interactively): ./console and enter command</li>
<li>Run hbnb(non-interactively): echo "<command>" | ./console.py</li>
</ul>

<h2>File Descriptions</h2>
<p>console.py - the console contains the entry point of the command interpreter. 
List of commands this console current supports:
</p>
<ul>
<li>EOF - exits console</li>
<li>quit - exits console</li>
<li><emptyline> - overwrites default emptyline method and does nothing</li>
<li>create - Creates a new instance of BaseModel, saves it (to the JSON file) and prints the id</li>
<li>destroy - Deletes an instance based on the class name and id (save the change into the JSON file).</li> 
<li>show - Prints the string representation of an instance based on the class name and id.</li>
<li>all - Prints all string representation of all instances based or not on the class name.</li> 
<li>update - Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file).</li> 
</ul>

<h4>models/ directory contains classes used for this project:</h4>
<p>base_model.py - The BaseModel class from which future classes will be derived</p>
<ul>
<li>def __init__(self, *args, **kwargs) - Initialization of the base model</li>
<li>def __str__(self) - String representation of the BaseModel class</li>
<li>def save(self)` - Updates the attribute updated_at with the current datetime</li>
<li>def to_dict(self) - returns a dictionary containing all keys/values of the instance</li>
</ul>

<p>Classes inherited from Base Model:</p>
<ul>
<li>amenity.py</li>
<li>city.py</li>
<li>place.py</li>
<li>review.py</li>
<li>state.py</li>
<li>user.py</li>
</ul>

<h4>models/engine directory contains File Storage class that handles JASON serialization and deserialization :</h4>
<p>file_storage.py-serializes instances to a JSON file & deserializes back to instances</p>
<ul>
<li>def all(self) - returns the dictionary __objects</li>
<li>def new(self, obj) - sets in __objects the obj with key <obj class name>.id</li>
<li>def save(self) - serializes __objects to the JSON file (path: __file_path)</li>
<li>def reload(self) - deserializes the JSON file to __objects</li>
</ul>

<h4>/tests directory contains all unit test cases for this project:</h4>
<p>test_models/test_base_model.py - Contains the TestBaseModel and TestBaseModelDocs classes
TestBaseModelDocs class:
</p>
<ul>
<li>def setUpClass(cls)- Set up for the doc tests</li>
<li>def test_pep8_conformance_base_model(self) - Test that models/base_model.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_base_model(self) - Test that tests/test_models/test_base_model.py conforms to PEP8</li>
<li>def test_bm_module_docstring(self) - Test for the base_model.py module docstring</li>
<li>def test_bm_class_docstring(self) - Test for the BaseModel class docstring</li>
<li>def test_bm_func_docstrings(self) - Test for the presence of docstrings in BaseModel methods</li>
</ul>

<p>TestBaseModel class:</p>
<ul>
<li>def test_is_base_model(self)` - Test that the instatiation of a BaseModel works</li>
<li>def test_created_at_instantiation(self) - Test created_at is a pub. instance attribute of type datetime</li>
<li>def test_updated_at_instantiation(self) - Test updated_at is a pub. instance attribute of type datetime</li>
<li>def test_diff_datetime_objs(self) - Test that two BaseModel instances have different datetime objects</li>
</ul>

<p>test_models/test_amenity.py - tests/test_models/test_amenity.py) - Contains the TestAmenityDocs class:<p>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_amenity(self) - Test that models/amenity.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_amenity(self) - Test that tests/test_models/test_amenity.py conforms to PEP8</li>
<li>def test_amenity_module_docstring(self) - Test for the amenity.py module docstring</li>
<li>def test_amenity_class_docstring(self) - Test for the Amenity class docstring</li>
</ul>

<p>test_models/test_city.py - Contains the TestCityDocs class:</p>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_city(self) - Test that models/city.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_city(self) - Test that tests/test_models/test_city.py conforms to PEP8</li>
<li>def test_city_module_docstring(self) - Test for the city.py module docstring</li>
<li>def test_city_class_docstring(self) - Test for the City class docstring</li>
</ul>

<p>test_models/test_file_storage.py - Contains the TestFileStorageDocs class:</p>
<ul>
<li>def setUpClass(cls)` - Set up for the doc tests
<li>def test_pep8_conformance_file_storage(self) - Test that models/file_storage.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_file_storage(self) - Test that tests/test_models/test_file_storage.py conforms to PEP8</li>
<li>def test_file_storage_module_docstring(self) - Test for the file_storage.py module docstring</li>
<li>def test_file_storage_class_docstring(self) - Test for the FileStorage class docstring</li>
</ul>

<p>test_models/test_place.py - Contains the TestPlaceDoc class:</p>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_place(self) - Test that models/place.py conforms to PEP8.</li>
<li>def test_pep8_conformance_test_place(self) - Test that tests/test_models/test_place.py conforms to PEP8.</li>
<li>def test_place_module_docstring(self) - Test for the place.py module docstring</li>
<li>def test_place_class_docstring(self) - Test for the Place class docstring</li>
</ul>

<p>test_models/test_review.py - Contains the TestReviewDocs class:</P>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_review(self) - Test that models/review.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_review(self) - Test that tests/test_models/test_review.py conforms to PEP8</li>
<li>def test_review_module_docstring(self) - Test for the review.py module docstring</li>
<li>def test_review_class_docstring(self) - Test for the Review class docstring</li>
</ul>

<p>test_models/state.py - Contains the TestStateDocs class:</p>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_state(self) - Test that models/state.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_state(self) - Test that tests/test_models/test_state.py conforms to PEP8</li>
<li>def test_state_module_docstring(self) - Test for the state.py module docstring</li>
<li>def test_state_class_docstring(self) - Test for the State class docstring</li>
</ul>

<p>test_models/user.py - Contains the TestUserDocs class:</p>
<ul>
<li>def setUpClass(cls) - Set up for the doc tests</li>
<li>def test_pep8_conformance_user(self) - Test that models/user.py conforms to PEP8</li>
<li>def test_pep8_conformance_test_user(self) - Test that tests/test_models/test_user.py conforms to PEP8</li>
<li>def test_user_module_docstring(self) - Test for the user.py module docstring</li>
<li>def test_user_class_docstring(self) - Test for the User class docstring</li>
</ul>

<h2>Examples of use</h2>
<pre>
<code>
"vagrantAirBnB_clone$./console.py
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
"
</code>
</pre>

<h2>Bugs<h2>

<p>No known bugs at this time.</p>

<h2>Original Authors</h2>
<p>Alexa Orrico - Github(https://github.com/alexaorrico) / Twitter(https://twitter.com/alexa_orrico)  
Jennifer Huang - Github(https://github.com/jhuang10123) / Twitter(https://twitter.com/earthtojhuang)
</p>

<p>Second part of Airbnb: Joann Vuong</P

<hr>
<h1>AirBnB Clone V3 - RESTful API</h1>
<h2>Description</h2>
<p>Integrating Flask web framework and REST into the Airbnb Clone project from a previous cohort.</P>
<hr>
<h2>Authors</h2>
<ul>
<li>Deyber Castañeda 1846@holbertonschool.com</li>
<li>Marcos Pimienta 1676@holbertonschool.com</li>
<hr>
<h2>License</h2>
<p>Public Domain. No copy write protection.</p>