#!/bin/bash

# Check if commit message is provided, otherwise use 'submit'
if [ -n "$1" ]; then
    commit_message="$*"
else
    commit_message='submit'
fi

git add .
git commit -m "$commit_message"
git push
