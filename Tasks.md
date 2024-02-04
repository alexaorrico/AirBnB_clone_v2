## Task 2 (Sarah)

**Summary**

-   Need to create a branch `storage_get_count`
-   Update DBStorage and FileStorage adding 2 methods...
    -   method to retrive one object and another to count objects in storage

**Files to create/Update - Including test files**

-   ~~`models/engine/db_storage.py`~~
-   ~~`models/engine/file_storage.py`~~
-   ~~`tests/test_models/test_engine/test_db_storage.py`~~
-   ~~`tests/test_models/test_engine/test_file_storage.py`~~

## Task 3 (Elvis)

**Summary**

-   Starting the api
-   creating a folder `api` at the root of the project with ....
-   Create a folder `v1` inside `api`
-   create a folder `views` inside `v1`.....

**Files to create/Update - Including test files**

-   ~~`api/__init__.py`~~
-   ~~`api/v1/__init__.py`~~
-   ~~`api/v1/views/__init__.py`~~
-   ~~`api/v1/views/index.py`~~
-   ~~`api/v1/app.py`~~

## Task 4 (Sarah)

**Summary**

-   Create an endpoint that retrieves the number of each objects by type
-   Route = `api/v1/stats`
-   You must use the newly added `count()`(Task 2) from `storage`

**Files to create**

-   ~~`api/v1/views/index.py`~~

## Task 5 (Sarah)

**Summary**

-   Create a handler for 404 errors that returns a JSON-formatted `404`
-   Content should be `"error: "Not found"`

**Files to create/Update**

-   ~~`api/v1/app.py`~~

## Task 6 (Sarah)

**Summary**

-   Create a new view for `State` objects that handles all default ....
-   retrieves the list of all `State` objects
-   retrieves `State` objects......

**Files to create/Update**

-   ~~`api/v1/views/states.py`~~
-   ~~`api/v1/views/__init__.py`~~

## Task 7 (Elvis)

**Files to create/Update**

-   ~~`api/v1/views/cities.py`~~
-   ~~`api/v1/views/__init__.py`~~

## Task 8

**Files to create/Update**

-   `api/v1/views/amenities.py`
-   `api/v1/views/__init__.py`

## Task 9

**Files to create/Update**

-   ~~`api/v1/views/users.py`~~
-   ~~`api/v1/views`~~

## Task 10

**Files to create/Update**

-   ~~`api/v1/views/places.py`~~
-   ~~`api/v1/views/__init__.py`~~

## Task 11

**Files to create/Update**

-   ~~`api/v1/views/places_reviews.py`~~
-   ~~`api/v1/views/__init__.py`~~

## Task 12

**Files to create/Update**

-   `api/v1/app.py`
