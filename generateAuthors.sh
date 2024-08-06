#!/bin/bash

# Use Git log to get a list of email addresses from the commit history
cat > "AUTHORS" <<- EOF
	# These individuals contributed to the hbnb project in this repository

	$(git log --format='%aN <%aE>' | LC_ALL=C.UTF-8 sort -uf)
EOF
