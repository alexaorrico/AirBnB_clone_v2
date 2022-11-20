#!/usr/bin/env bash
# handle git operations
add(){ git add .; }
commit(){ m=$message; git commit -m "$m"; }
push(){ git push; }
pull(){ git pull; }
message="fixed bug in project"
if [ -n "$2" ]
then
	message="$2"
fi
if [ $# -lt 1 ]
then
	echo "Usage: $0 [a | c | ps | pl] [message]"
	# a - To only
	# c - To add and comit only
	# ps - To add, commit and push
	# pl - To add commit and pull
else
	case "$1" in
		a)
			add;;
		c)
			add && commit "$message" ;;
		ps)
			add && commit "$message" && push
			;;
		pl)
			add && commit "$message" && pull
			;;
		*)
			echo "Usage: $0 [a | c | ps | pl] [message]"
	esac
fi
