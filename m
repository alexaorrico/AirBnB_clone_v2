#!/bin/bash
read -p "type your commit message : " mm
git add .
git commit -m "$mm"
git push
