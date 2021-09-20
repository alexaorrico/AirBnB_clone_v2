Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@livejo 
kalkidan999
/
AirBnB_clone_v3
Public
forked from alexaorrico/AirBnB_clone_v2
0
0783
Code
Pull requests
Actions
Projects
Wiki
Security
Insights
AirBnB_clone_v3
/
tests
/
test_models
/
test_engine
/
test_file_storage.py
in
storage_get_count
 

Spaces

11

No wrap
1
#!/usr/bin/python3
2
"""
3
Contains the TestFileStorageDocs classes
4
"""
5
​
6
from datetime import datetime
7
import inspect
8
import models
9
from models.engine import file_storage
10
from models.amenity import Amenity
11
from models.base_model import BaseModel
12
from models.city import City
13
from models.place import Place
14
from models.review import Review
15
from models.state import State
16
from models.user import User
17
import json
18
import os
19
import pep8
20
import unittest
21
FileStorage = file_storage.FileStorage
22
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
23
           "Place": Place, "Review": Review, "State": State, "User": User}
24
​
25
​
26
class TestFileStorageDocs(unittest.TestCase):
27
    """Tests to check the documentation and style of FileStorage class"""
28
    @classmethod
29
    def setUpClass(cls):
30
        """Set up for the doc tests"""
31
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)
32
​
33
    def test_pep8_conformance_file_storage(self):
34
        """Test that models/engine/file_storage.py conforms to PEP8."""
35
        pep8s = pep8.StyleGuide(quiet=True)
36
        result = pep8s.check_files(['models/engine/file_storage.py'])
37
        self.assertEqual(result.total_errors, 0,
38
                         "Found code style errors (and warnings).")
39
​
40
    def test_pep8_conformance_test_file_storage(self):
41
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
42
        pep8s = pep8.StyleGuide(quiet=True)
43
        result = pep8s.check_files(['tests/test_models/test_engine/\
44
test_file_storage.py'])
45
        self.assertEqual(result.total_errors, 0,
@livejo
Commit changes
Commit summary
Create test_file_storage.py
Optional extended description
Add an optional extended description…
 Commit directly to the storage_get_count branch.
 Create a new branch for this commit and start a pull request. Learn more about pull requests.
 
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
