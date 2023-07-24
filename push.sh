#!/bin/bash
#Script pushes code to github
git add .
echo 'Enter commit title: '
read commit_title
git commit -m "$commit_title"
result=$?
if [ $result -eq 0 ]; then	
	git push
else	
	echo 'Commit Failed'
fi
