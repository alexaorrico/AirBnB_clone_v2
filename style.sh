#!/usr/bin/env bash

chmod a+x $(find . -name '*.py')
pycodestyle $(find . -name '*.py')
