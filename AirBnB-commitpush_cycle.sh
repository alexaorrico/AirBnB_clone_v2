#!/bin/bash
# Git Staging Automation (Authour - Ernest Shongwe created during JPMC
# internship, modified during AirBnB Clone v3 @ ALX Africa

# Lock file definition
lock_file="/tmp/push_script.lock"

# Checks if lock file exists, indicating another instance is already running
if [ -e "$lock_file" ]; then
    echo "Another instance of the script is already running. Exiting."
    exit 1
fi

# Creates lock file
touch "$lock_file"

# Defines branch name
branch_name="storage_get_count"

# Stages changes
git add .

# Checks if branch exists
if git rev-parse --verify --quiet "$branch_name"; then
    echo "Branch '$branch_name' already exists. Pulling changes from the remote repository..."
    git checkout "$branch_name" || { echo "Failed to switch to branch '$branch_name'."; rm "$lock_file"; exit 1; }
    git pull origin "$branch_name" || { echo "Failed to pull changes from remote repository."; rm "$lock_file"; exit 1; }
else
    echo "Branch '$branch_name' does not exist. Creating it..."
    git checkout -b "$branch_name" || { echo "Failed to create branch '$branch_name'."; rm "$lock_file"; exit 1; }
fi

# Commit changes with a timestamp (only edit this in this file: the commit message)
timestamp=$(date +"%Y-%m-%d %T")
commit_message="Task <number>: <task title> - Automated commit at $timestamp"
git commit -m "$commit_message"

# Push changes to the branch, handling conflicts
if ! git push --set-upstream origin "$branch_name"; then
    echo "Failed to push changes to branch '$branch_name'. Resolving conflicts..."
    
    # Attempt to pull changes again
    if ! git pull origin "$branch_name"; then
        echo "Failed to pull changes from remote repository. Manual intervention required."
        rm "$lock_file"
        exit 1
    fi
    
    # Resolve conflicts
    # (This is where you would handle the conflicts, either manually or using automated tools)
    
    # Once conflicts are resolved, stage changes and commit
    git add .
    git commit -m "Resolved conflicts in '$branch_name'"
    
    # Push changes again
    git push origin "$branch_name" || { echo "Failed to push changes after conflict resolution."; rm "$lock_file"; exit 1; }
fi

# Remove lock file
rm "$lock_file"

# Confirmation
echo "Changes pushed to branch '$branch_name'."
