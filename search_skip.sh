#!/bin/bash

# Set the directory to search
directory="$1"

# Search for files containing the string "@unittest.skip"
grep -r "@unittest.skip" "$directory"

