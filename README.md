<img src="https://github.com/johncoleman83/AirBnB_clone/blob/master/dev/HBTN-hbnb-Final.png" width="160" height=auto />

# AirBnB Clone Phase #1

: python BaseModel Class, unittests, python CLI, & web static

## Description

Project attempts to clone the the AirBnB application and website, including the
database, storage, RESTful API, Web Framework, and Front End.

## Environment

* __OS:__ Ubuntu 14.04 LTS
* __language:__ Python 3.4.3
* __style:__ PEP 8 (v. 1.7.0)

<img src="https://github.com/johncoleman83/AirBnB_clone/blob/master/dev/hbnb_step5.png" />

## Testing

#### NOTE: YOU MUST RUN THE SQL SCRIPT `setup_mysql_test.sql` RO RUN THE UNIT TESTS.
```
$ cat setup_mysql_test.sql | mysql -u root -p
```


#### `unittest`

This project uses python library, `unittest` to run tests on all python files.
All unittests are in the `./tests` directory with the command:

* `python3 -m unittest discover -v ./tests/`

The bash script `init_test.sh` executes all these tests:

  * checks `pep8` style

  * runs all unittests

  * runs all w3c_validator tests

  * cleans up all `__pycache__` directories and the storage file, `file.json`

**Usage:**

```
$ ./dev/init_test.sh
```

#### CLI Interactive Tests

This project uses python library, `cmd` to run tests in an interactive command
line interface.  To begin tests with the CLI, run this script:

```
$ ./console.py
```

* For a detailed description of all tests, run these commands inside the
custom CLI:

```
$ ./console.py
(hbnb) help help
List available commands with "help" or detailed help with "help cmd".
(hbnb) help

Documented commands (type help <topic>):
========================================
Amenity    City  Place   State  airbnb  create   help  show
BaseModel  EOF   Review  User   all     destroy  quit  update

(hbnb) help User
class method with .function() syntax
        Usage: User.<command>(<id>)
(hbnb) help create
create: create [ARG]
        ARG = Class Name
        SYNOPSIS: Creates a new instance of the Class from given input ARG
```

* Tests in the CLI may also be executed with this syntax:

  * **destroy:** `<class name>.destroy(<id>)`

  * **update:** `<class name>.update(<id>, <attribute name>, <attribute value>)`

  * **update with dictionary:** `<class name>.update(<id>, <dictionary representation>)`


#### Continuous Integration

Uses [Travis-CI](https://travis-ci.org/) to run all tests on all commits to the
github repo

## Running

Clone the Repo
```
$ git clone https://github.com/glyif/AirBnB_clone_v3 && cd AirBnB_clone_v3
```

Install Dependencies
```
$ pip3 install -r requirements.txt
```

VirtualEnv Alternative
```
$ virtualenv -p $(which python3) env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Running Console
```
$ ./console.py
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py
```

Running Flask API
```
$ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
```

To exit out of the virtualenv, use:
```
$ deactivate
```

### Docker Integration
To run with docker, it's very simple.

NOTE: You will need to have docker and docker-compose installed

First, build all of the images. (console, db, api)
```
$ docker-compose build --no-cache
```

Then you can just run the images
```
$ docker-compose up -d
```

To use the console, you'll need to run:
```
$ docker exec -it <container_id> /bin/bash
```
NOTE: you will need to replace <container_id> with the actual console container id

NOTE: TESTING WITH DOCKERHUB AND RANCHER
## API Documentation
There is a postman json in side the API folder that you can import to check out the api endpoints, or you can go to [the online version](https://documenter.getpostman.com/view/1535334/airbnb_clone_v3/6tc3iuA)

Swagger documentation will soon come.

## Authors

* MJ Johnson, [@mj31508](https://github.com/mj31508)
* David John Coleman II, [davidjohncoleman.com](http://www.davidjohncoleman.com/)
* Kimberly Wong, [kjowong](http://github.com/kjowong) | [@kjowong](http://twitter.com/kjowong) | [kjowong@gmail.com](kjowong@gmail.com)
* Carrie Ybay, [hicarrie](http://github.com/hicarrie) | [@hicarrie_](http://twitter.com/hicarrie_)
* Naomi Sorrell, [NamoDawn](https://github.com/NamoDawn) | [@NamoDawn](https://twitter.com/NamoDawn)
* Bobby Yang, [glyif](https://github.com/glyif) | [@bobstermyang](https://twitter.com/bobstermyang)

## License

Public Domain, no copyright protection
