#!/usr/bin/env bash
# This initializes testing suite.
# Checks pep8 style of all python files
# also runs all unittests
pep8 . && python3 -m unittest discover -v ./tests/ \
    && ./dev/w3c_validator.py \
        $(find ./web_static -maxdepth 1 -name "*.html" -type f ! -name "4*") \
    && ./dev/w3c_validator.py \
	$(find ./web_static/styles -maxdepth 1 -name "*.css" -type f)

# stores the return value
ret_val=$?

# clears file.json
> ./dev/file.json

# removes __pycache__ folder
py3clean .

# exits with status from tests
exit "$ret_val"
