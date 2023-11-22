# AirBnB Clone V3 Project

## Authors
- [Fox Galileo](https://github.com/bansheegalileo)
- [Taylor Poe](https://github.com/TPoe25)

## Description
This project is a continuation of the AirBnB clone project. We are building upon the previous version (holbertonschool-AirBnB_clone_v2) and adding new features, tests, and improvements.

## Table of Contents
- [General Information](#general-information)
- [Requirements](#requirements)
- [Tasks](#tasks)
	- [Restart from scratch!](#task-1-restart-from-scratch)
	- [Never fail!](#task-2-never-fail)
	- [Code review](#task-3-code-review)
	- [Improve storage](#task-4-improve-storage)
	- [Status of your API](#task-5-status-of-your-api)
	- [Some stats?](#task-6-some-stats)
	- [Not found](#task-7-not-found)
	- [State](#task-8-state)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](##tests)
- [Code Review](#code-review)


## General Information
Building RESTful web services, like other programming skills is **part art, part science**. As the Internet industry progresses, creating a REST API becomes more concrete with emerging best practices. As RESTful web services don't follow aprescribed standard except for HTTP, it's important to build your RESTful API in accordance with industry best practices to ease development and increase client adoptionation. - [https://www.restapitutorial.com/]


## Requirements
### Python Scripts
- Allowed editors: vi, vim, emacs
- All your files will be interpreted/compiled on Ubuntu 20.04 LTS using python3 (version 3.8.5)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/python3`
- A README.md file, at the root of the folder of the project, is mandatory
- Your code should use the pycodestyle (version 2.7.*)
- All your files must be executable
- The length of your files will be tested using wc
- All your modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)' and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class, or method (the length of it will be verified)

### Python Unit Tests
- Allowed editors: vi, vim, emacs
- All your files should end with a new line
- All your test files should be inside a folder tests
- You have to use the unittest module
- All your test files should be python files (extension: .py)
- All your test files and folders should start by test_
- Your file organization in the tests folder should be the same as your project
- All your tests should be executed by using this command: `python3 -m unittest discover tests`


## Tasks
### Task 1: Restart from scratch!
- Fork the codebase and make necessary updates.
- Update the repository name to holbertonschool-AirBnB_clone_v3.
- Update the README.md file with new information.

### Task 2: Never fail!
- Ensure all current tests pass.
- Add new tests as much as you can.

### Task 3: Code review
- Review a peer’s pull request on the branch storage_get_count.
- Accept the pull request with your review in the comments.

### Task 4: Improve storage
- Update DBStorage and FileStorage, adding two new methods.
- Implement the following methods in the branch storage_get_count:
    - A method to retrieve one object:
        ```python
        def get(self, cls, id):
            """Retrieve one object."""
        ```
    - A method to count the number of objects in storage:
        ```python
        def count(self, cls=None):
            """Count the number of objects in storage."""
        ```
- Add new tests for these 2 methods on each storage engine.

### Task 5: Status of your API
- Create a Flask API endpoint to return the status of your API.
- Endpoint: `GET /api/v1/status`
- Example response:
    ```json
    {
      "status": "OK"
    }
    ```
- Update the README.md file accordingly.

### Task 6: Some stats?
- Create an endpoint to retrieve the number of each object type.
- Endpoint: `GET /api/v1/stats`
- Use the newly added count() method from storage.
- Example response:
    ```json
    {
      "amenities": 47, 
      "cities": 36, 
      "places": 154, 
      "reviews": 718, 
      "states": 27, 
      "users": 31
    }
    ```

### Task 7: Not found
- Create a handler for 404 errors in JSON format.
- Endpoint: Any non-existing endpoint (e.g., `GET /api/v1/nop`)
- Example response:
    ```json
    {
      "error": "Not found"
    }
    ```
- Update the README.md file accordingly.

### Task 8: State
- Create a new view for State objects that handles default RESTful API actions.
- Endpoint: `/api/v1/states`
- Example responses:
    - `GET /api/v1/states`: List of all State objects.
    - `GET /api/v1/states/<state_id>`: Retrieve a specific State object.
    - `DELETE /api/v1/states/<state_id>`: Delete a specific State object.
    - `POST /api/v1/states`: Create a new State object.
    - `PUT /api/v1/states/<state_id>`: Update a specific State object.
- Example request:
    ```bash
    $ curl -X GET http://0.0.0.0:5000/api/v1/states/
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
        "id": "1a9c29c7-e39c-4840-b5f
        
## Installation
To install Flask, run the following command:
```bash
$ pip3 install Flask
