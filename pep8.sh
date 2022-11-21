#!/usr/bin/env bash

echo "Fixing pep8 warnings >>>"
find . -type f -name '*.py' ! -path '*/migrations/*' -exec autopep8 --in-place --aggressive --aggressive '{}' \;

echo "Checking pycodestyle >>>"
find . -type f -name '*.py' ! -path '*/migrations/*' -exec pycodestyle --first '{}' \;
