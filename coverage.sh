#!/usr/bin/env bash

# Script to automate coverage
# ensure coverage module is installed

python3 -m coverage run -m unittest

python3 -m coverage html
