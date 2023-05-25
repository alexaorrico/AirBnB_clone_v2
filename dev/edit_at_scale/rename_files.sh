#!/usr/bin/env bash
for f in $(ls *-* | grep -v "~$"); do
    new_name=$(echo "$f" | cut -d'-' -f2)
    mv "$f" "test_$new_name"
done
