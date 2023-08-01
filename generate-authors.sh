#!/bin/sh
# a script that autogenerate GitHub authors/collaboratos' name and email.
git log --format='%aN <%aE>' | sort -u > AUTHORS
