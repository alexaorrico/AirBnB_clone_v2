
<p align="center">
    <img src="https://i.imgur.com/JOhaZ5m.png">
</p>

# Description

The goal of the HBnB project is to deploy a simple clone of AirBnB on our own server.
This project is built over 4 months as part of the curriculum of the first year at Alx Engineering Program)).

At the end of the 4 months, the project will have:
- A command interpreter to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
- A website (the front-end) that shows the final product to everybody: static and dynamic
- A database or files that store data (data = objects)
- An API that provides a communication interface between the front-end and the data (retrieve, create, delete, update them)

Here's a simple diagram of the entire stack of the final product:

<p>
    <img src="https://i.imgur.com/sQ4tQRX.png">
</p>

# The Web Framework

Flask is the web framework used for the HBnB project.
In the [web_flask](./web_flask) are all the python scripts used to start a Flask app.

Usage:

- Dump data in the MySQL database with [10-dump.sql](./10-dump.sql) or [100-dump.sql](./100-dump.sql), for scripts [10-hbnb_filters.py](.10-hbnb_filters.py) and [100-hbnb.py](./100-hbnb.py) respectively:
```
cat 100-dump.sql | mysql -uroot -p
```

- Set the environment variables and execute the Flask scripts like this:
```
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m web_flask.100-hbnb
```

- In the browser, type:
```
http://0.0.0.0:5000/hbnb
```
You should see the rendered web page!

# The Storage system

HBnB has two storage types: a File Storage and a DataBase storage.
The folder [engine](./models/engine/) contains those storage types definitions.
Here is a representation of all the data:

<p>
    <img src="https://i.imgur.com/eNZMRuS.jpg">
</p>

## File Storage

The File Storage system manages the serialization and deserialization of all the data, following a JSON format.

A FileStorage class is defined in [file_storage.py](./models/engine/file_storage.py) with methods to follow this flow:
```<object> -> to_dict() -> <dictionary> -> JSON dump -> <json string> -> FILE -> <json string> -> JSON load -> <dictionary> -> <object>```

If the environment variable **HBNB_TYPE_STORAGE** is set to 'file', the [__init__.py](./models/__init__.py) file instantiates the FileStorage class called **storage**, followed by a call to the method reload() on that instance.
This allows the storage to be reloaded automatically at initialization, which recovers the serialized data.

## DataBase Storage

The DataBase Storage system manages communication to and from a MySQL server, where data will be stored in a database depending on the **HBNB_MYSQL_DB** variable value.

A DBStorage class is defined in [db_storage.py](./models/engine/db_storage.py) and uses the SQAlchemy module to interact with MySQL.

If the environment variable **HBNB_TYPE_STORAGE** is set to 'db', the [__init__.py](./models/__init__.py) file instantiates the DBStorage class called **storage**, followed by a call to the method reload() on that instance.
This allows the storage to be reloaded automatically at initialization, which recovers the data from the defined database.

To run any script with the DataBase storage, declare those environment variables:
```
HBNB_MYSQL_USER=hbnb_dev
HBNB_MYSQL_PWD=hbnb_dev_pwd
HBNB_MYSQL_HOST=localhost
HBNB_MYSQL_DB=hbnb_dev_db
HBNB_TYPE_STORAGE=db
```

# The Console

This is the console /command interpreter for the Holberton Airbnb clone project. The console can be used to store objects in and retrieve objects from a JSON.

### Supported classes:
* BaseModel
* User
* State
* City
* Amenity
* Place
* Review

### Commands:
* create - create an object
* show - show an object (based on id)
* destroy - destroy an object
* all - show all objects, of one type or all types
* quit/EOF - quit the console
* help - see descriptions of commands

To start, navigate to the project folder and enter `./console.py` in the shell.

#### Create
`create <class name>`
Ex:
`create BaseModel`

#### Show
`show <class name> <object id>`
Ex:
`show User my_id`

#### Destroy
`destroy <class name> <object id>`
Ex:
`destroy Place my_place_id`

#### All
`all` or `all <class name>`
Ex:
`all` or `all State`

#### Quit
`quit` or `EOF`

#### Help
`help` or `help <command>`
Ex:
`help` or `help quit`

Additionally, the console supports `<class name>.<command>(<parameters>)` syntax.
Ex:
`City.show(my_city_id)`

# Tests

All unittests can be found in the [tests](./tests) directory.

# Author
Chukuma Uche Daniel
