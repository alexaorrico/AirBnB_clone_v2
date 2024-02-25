#!/bin/bash
git add .
read -p "commit message: " message
git commit -m "$message"
git push
