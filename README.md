# Airbnb Clone API

## Overview
This project is an implementation of an API for an Airbnb clone. The API provides various endpoints to interact with data related to Airbnb-like accommodations, including states, cities, places, users, reviews, and amenities.

## Requirements
- Python Scripts
  - Operating System: Ubuntu 20.04 LTS
  - Python Version: 3.4.3 or higher
  - Code should be PEP 8 compliant (style version 1.7)
  - All Python scripts should have a shebang line at the beginning: `#!/usr/bin/python3`
  - All Python scripts should end with a new line
  - All scripts must be executable
  - All modules, classes, and functions should have appropriate documentation
  - A `README.md` file at the root of the project is mandatory

- Python Unit Tests
  - Use the `unittest` module for writing tests
  - All test files should be inside a folder named `tests`
  - Test files should have the extension `.py`
  - Test files and folders should start with `test_`
  - Organize test files in a manner that mirrors the project's file structure
  - Run tests using the command: `python3 -m unittest discover tests`

## Project Structure
The project is structured as follows:

```
- api/
    - __init__.py
    - v1/
        - __init__.py
        - app.py
        - views/
            - __init__.py
            - index.py
- models/
    - __init__.py
    - ...
- tests/
    - test_models/
        - test_engine/
            - test_db_storage.py
            - test_file_storage.py
        - test_base_model.py
        - ...
    - ...
```

## API Endpoints
### Status
- Route: `/api/v1/status`
- Description: Returns the status of the API.
- Example:
  ```
  $ curl -X GET http://0.0.0.0:5000/api/v1/status
  {
    "status": "OK"
  }
  ```

### Object Counts
- Route: `/api/v1/stats`
- Description: Retrieves the number of each object type available in the API, using the `count()` method from storage.
- Example:
  ```
  $ curl -X GET http://0.0.0.0:5000/api/v1/stats
  {
    "amenities": 47,
    "cities": 36,
    "places": 154,
    "reviews": 718,
    "states": 27,
    "users": 31
  }
  ```

## Getting Started
To run the API, follow these steps:

1. Set up the necessary environment variables:
   - `HBNB_MYSQL_USER`
   - `HBNB_MYSQL_PWD`
   - `HBNB_MYSQL_HOST`
   - `HBNB_MYSQL_DB`
   - `HBNB_TYPE_STORAGE`
   - `HBNB_API_HOST` (optional, default: '0.0.0.0')
   - `HBNB_API_PORT` (optional, default: 5000)

2. Run the Flask application:
   ```
   $ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db HBNB_API_HOST=0.0.0.0 HBNB_API_PORT=5000 python3 -m api.v1.app
   ```

3. Access the API endpoints as described in the examples above.

## Running Tests
To run the unit tests, use the following command:
```
$ python3 -m unittest discover tests
```


## Authors
Siaw Nicholas - [Github](https://github.com/ayequill)
Jennifer Huang - [Github](https://github.com/kaleabendrias)

## License
Public Domain. No copy write protection. 
