language: python

dist: "trusty"

python:
  - "3.4"

services:
  - mysql

notifications:
  email: false

before_install:
  - sudo apt-get update
  - sudo pip install --upgrade pip
  - sudo apt-get install --upgrade python3-pip

install: "pip install -r requirements.txt"

script: ./dev/travis_init_test.sh
