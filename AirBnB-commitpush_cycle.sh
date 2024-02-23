#!/bin/bash

//push script//

# Define the branch name
branch_name="storage_get_count"

# Check if the branch exists
if git rev-parse --verify --quiet "$branch_name"; then
	    echo "Branch '$branch_name' already exists."
    else
	        echo "Branch '$branch_name' does not exist. Creating it..."
		    git checkout -b "$branch_name" || { echo "Failed to create branch '$branch_name'."; exit 1; }
fi

# Pull changes from the remote repository
git pull origin "$branch_name" || { echo "Failed to pull changes from remote repository."; exit 1; }

# Push changes to the branch
git push --set-upstream origin "$branch_name" || { echo "Failed to push changes to branch '$branch_name'."; exit 1; }

# Confirmation
echo "Changes pushed to branch '$branch_name'."
