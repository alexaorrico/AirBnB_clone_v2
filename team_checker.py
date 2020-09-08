#!/usr/bin/python3
"""
Automates some tasks

To use the script with a single command type the following:
$ chmod +x team_checker.py
$ alias <command_name>='./team_checker.py'
$ source ~/.bashrc

"""
import os
import sys
import importlib


# pep8 all .py files
print("\n\t======== PEP8 CHECK ========\n")
os.system("pep8 $(find . -name \"*.py\")")

# Run unittest
print("\n\t========  UNITTEST CHECK ========\n")
os.system("python3 -m unittest discover tests 2>&1 /dev/null | tail -n 1")

# Check for Documentation
packages = [
    {"models": [
                {"base_model": ["BaseModel"]},
                {"amenity": ["Amenity"]},
                {"city": ["City"]},
                {"place": ["Place"]},
                {"review": ["Review"]},
                {"state": ["State"]},
                {"user": ["User"]}
                ]},
    {"models.engine": [
                {"file_storage": ["FileStorage"]},
                {"db_storage": ["DBStorage"]}]},
    {"tests.test_models": [
                {"test_amenity": ["TestAmenityDocs"]},
                {"test_base_model": ["TestBaseModelDocs", "TestBaseModel"]},
                {"test_city": ["TestCityDocs", "TestCity"]},
                {"test_place": ["TestPlaceDocs", "TestPlace"]},
                {"test_review": ["TestReviewDocs", "TestReview"]},
                {"test_state": ["TestStateDocs", "TestState"]},
                {"test_user": ["TestUserDocs", "TestUserDocs"]}]}]

print("\n\t======== Documentation CHECK ========\n")
for package in packages:
    for path, modules in package.items():
        for module in modules:
            for k, v in module.items():
                mod = importlib.import_module('{}.{}'.format(path, k))
                if mod:
                    print("[Found] - {} Module docs".format(k))
                else:
                    print("[Not Found] - {} Module docs".format(k))
                for m_class in v:
                    doc = eval("mod.{}.__doc__".format(m_class))
                    if doc:
                        print("[Found] - {} class docs".format(m_class))
                    else:
                        print("[Not Found] - {} class docs".format(m_class))
print()
