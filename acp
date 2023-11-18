#!/bin/bash

# parse if file is added after calling function
if [ "$#" -gt 0 ]; then
    for file in "$@"; do
        # Check if file exists
        if [ -f "$file" ]; then
            git add "$file"
            echo "Added file: $file"
        else
            echo "File $file does not exist. Check your files and give it another go :)"
            exit 1
        fi
    done
else
    # if no file(s) added, ask if they want to add all files
    while true; do
        read -p "You cool with adding everything in here? (y/n) or press enter to add all: " add_all
        case $add_all in
            [Yy]* | "" ) git add .; break;;
            [Nn]* ) echo -e "\nIf you need to only add some files, here's the proper usage:\n
            --------------------------
            acp /file1 /file2
            --------------------------
            \nGive a whirl!"; exit 0;;
            * );;
        esac
    done
fi
# Ask for initial
read -p "Enter your initial: " initial

# Get current date and time
current_date_time=$(date '+%m/%d %I:%M %p')

# ask for a commit message
while true; do
    read -p "Commit message: " commit_msg
    if [ -z "$commit_msg" ]; then
        echo -e "Oops, gotta have a commit message!\n"
    else
        # Use initial and current date and time in commit message
        git commit -m "$initial - $current_date_time - $commit_msg"
        break
    fi
done

# ask if they wants to push
while true; do
    read -p "Committed! Ready to push? (y/n) or press enter to push: " push_repo
    case $push_repo in
        [Yy]* | "")
            echo "Okay!"
            if ! git push; then
                # if git push fails, let em know!
                echo -e "Rut-Roh, something's funky with git, the push was unsuccessful!\n"
                exit 1
            fi
            break
            ;;
        [Nn]* ) echo "Sure thing homie! Don't forget to push later!"; exit 0;;
        * ) echo "Oops, lets try that again. ";;
    esac
done
# To make this executable from anywhere on a MacOS,
# copy the following commands:
# sudo mv acp.sh /usr/local/bin
# sudo chmod +x /usr/local/bin/acp.sh
# sudo ln -s /usr/local/bin/acp.sh/usr/local/bin/acp
