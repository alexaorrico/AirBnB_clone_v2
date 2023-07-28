# AirBnB clone - RESTful API

<div align="center">
 <img src="./hack/hbnb_console.png" height="150" width="600" />
</div>

> `OOP`, `Back-end`, `SQL` - `MySQL`, `ORM`-`SQLAlchemy`, `Flask`-`API`

### Background

This is a clone of the [AirBnB website](https://www.airbnb.com/). This specific part covers a RESTful API - based design of the project; 

#### What a RESTful API IS:

***REST (Representational State Transfer)*** is an architectural style used in APIs. It uses standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations on resources. REST is the most popular API architecture for transferring data over the internet. In a RESTful context, resources are accessible via endpoints, and operations are performed on those resources with standard HTTP methods such as GET, POST, PUT, and DELETE.
A RESTful API architecture is Resource-based, a resource is an object and can be access by a `URI`. An object is “displayed”/transferred via a representation (typically JSON).


---
### Basic Functionality

`Specifications`:
```bash
    - A command interpreter to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
    - A website (the front-end) that shows the final product to everybody: static and dynamic
    - A database or files that store data (data = objects)
    - An API that provides a communication interface between the front-end and your data (retrieve, create, delete, update them):
        - expose all your objects stored via a JSON web interface
        - manipulate your objects via a RESTful API
```

---
### File Hierarchy:

> Repository Contents Info:  
>> This section is all file information.
```bash
.
├── AUTHORS - Docker specified formatted file for contributors
├── README.md - project documentation.
├── console.py - single-use command interpreter(uses Python `cmd` module).
├── models/ - the main driver of the project; lays out Python Object Orientation, initialization,  serialization, (de)serialization etc.
│   ├── __init__.py - effectively make a `Python` Package out of these modules, unique FileStorage instance for app
│   ├── base_model.py  - includes base (class) model ; for subclassing/inheritance - is the superclass.
│   ├── user.py - sample file with subclass of BaseModel(from module base_model)
│   ├── engine/ - abstracted storage engine/system for persisting data.
│   │   ├── __init__.py - effectively make a `Python` Package out of these modules
│   │   └── file_storage.py - module with methodes meant to interact with file storage(read from/write to JSON file), and models
└── tests/ - directory for unit testing, test cases/test suites etc.
    ├── __init__.py - effectively make a `Python` Package out of these modules, for Python test discovery.
    └── test_models/ - files that test models eg test_base_model.py, test_user.py, test_review.py
        └── __init__.py - effectively make a `Python` Package out of these modules, for Python test discovery.

├── web_flask
│   ├── *.py - Flask routing files
│   ├── README.md
│   ├── __init__.py
│   ├── static
│   │   ├── images
│   │   │   └── logos/icons
│   │   └── styles - Cascading Style Sheets
│   │       └── *.css
│   └── templates - Jinja templating
│       └── *.html
└── web_static
    └── Frontend of the application directory hosting static files: CSS, HTML, Images.
```


## Command Interprter
> `command-line interface`<br/>
> a shell implementation that uses the `Python` module `cmd`, which provides a simple framework for writing line-oriented command interpreters.



## `Shell` Behavior:
Is a `CRUD` simulated behavior - operations on objects in command-line.

> **Note**:  
> start interpreter in interactive mode: `./console.py`;- quit interpreter: type `quit` or `EOF`, or press `Ctrl + D` <br/>
> sample interpreter features: `create`, `show`, `update`, `destroy`, etc<br/>  

### Usage:
```bash
# run the interpreter in interactive mode:
/AirBnB_clone$ ./console.py
```
```bash
# prompt designates you are in the "HBnB" console
(hbnb)
```

##### Commands
> There are a variety of commands available within the console program.  

    * create - Creates an instance based on given class

    * destroy - Destroys an object based on class and UUID

    * show - Shows an object based on class and UUID

    * all - Shows all objects the program has access to, or all objects of a given class

    * update - Updates existing attributes an object based on class name and UUID

    * quit - Exits the program (EOF will as well)


##### Alternative Syntax
Users are able to issue a number of console command using an alternative syntax:

	`Syntax`: <class_name>.<command>([<id>[name_arg value_arg]|[kwargs]])
Advanced syntax is implemented for the following commands: 

    * all - Shows all objects the program has access to, or all objects of a given class

	* count - Return number of object instances by class

    * show - Shows an object based on class and UUID

	* destroy - Destroys an object based on class and UUID

    * update - Updates existing attributes an object based on class name and UUID

<br>
<br>

<center> <h2>Command Palette Examples</h2> </center>
<h3>Primary Command Syntax</h3>

###### Example 0: Create an object
Usage: create <class_name>
```
(hbnb) create BaseModel
```
```
(hbnb) create BaseModel
3aa5babc-efb6-4041-bfe9-3cc9727588f8
(hbnb)                   
```
###### Example 1: Show an object
Usage: show <class_name> <_id>

```
(hbnb) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
[BaseModel] (3aa5babc-efb6-4041-bfe9-3cc9727588f8) {'id': '3aa5babc-efb6-4041-bfe9-3cc9727588f8', 'created_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96959), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96971)}
(hbnb)  
```
###### Example 2: Destroy an object
Usage: destroy <class_name> <_id>
```
(hbnb) destroy BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
(hbnb) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
** no instance found **
(hbnb)   
```
###### Example 3: Update an object
Usage: update <class_name> <_id>
```
(hbnb) update BaseModel b405fc64-9724-498f-b405-e4071c3d857f first_name "person"
(hbnb) show BaseModel b405fc64-9724-498f-b405-e4071c3d857f
[BaseModel] (b405fc64-9724-498f-b405-e4071c3d857f) {'id': 'b405fc64-9724-498f-b405-e4071c3d857f', 'created_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729889), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729907), 'first_name': 'person'}
(hbnb)
```

<h3>Alternative Syntax</h3>

###### Example 0: Show all User objects
Usage: <class_name>.all()
```
(hbnb) User.all()
["[User] (99f45908-1d17-46d1-9dd2-b7571128115b) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 34, 92071), 'id': '99f45908-1d17-46d1-9dd2-b7571128115b', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 34, 92056)}", "[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```

###### Example 1: Destroy a User
Usage: <class_name>.destroy(<_id>)
```
(hbnb) User.destroy("99f45908-1d17-46d1-9dd2-b7571128115b")
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```
###### Example 2: Update User (by attribute)
Usage: <class_name>.update(<_id>, <attribute_name>, <attribute_value>)
```bash
(hbnb) User.update("98bea5de-9cb0-4d78-8a9d-c4de03521c30", name "Todd the Toad")
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'name': 'Todd the Toad', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```

###### Example 3: Update User (by dictionary)
Usage: <class_name>.update(<_id>, <dictionary>)
```bash
(hbnb) User.update("98bea5de-9cb0-4d78-8a9d-c4de03521c30", {'name': 'Fred the Frog', 'age': 9})
(hbnb)
(hbnb) User.all()
(hbnb) ["[User] (98bea5de-9cb0-4d78-8a9d-c4de03521c30) {'updated_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134362), 'name': 'Fred the Frog', 'age': 9, 'id': '98bea5de-9cb0-4d78-8a9d-c4de03521c30', 'created_at': datetime.datetime(2020, 2, 19, 21, 47, 29, 134343)}"]
```
<br>

---
## Python Unit Tests
> uses the `unittest` module for testing.<br/>
> `path` to test files/for test coverage - directory: `tests/test_models`

Running tests using Python test discovery...

```bash
# execute tests using this command for all tests: 
$ python3 -m unittest discover tests
# test file by file by using this command: 
$ python3 -m unittest tests/test_models/test_base_model.py
```

## Authors

You can find a list of contributors/project developers in the [authors](./AUTHORS) file.
