#!/usr/bin/env bash

file="$(find . -name '.git')"
while read -r line
do
	rm -rf $line
done <<< $file
