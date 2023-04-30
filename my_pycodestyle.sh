#!/usr/bin/env bash
# custom automator for pycodestyle check for the current project

pycodestyle -v $(ls -R *.py ./*/*.py ./*/*/*.py ./*/*/*/*.py | tr "\n" ' ')
