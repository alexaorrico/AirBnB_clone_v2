#!/bin/bash

# download 7-dump
curl -o 7-dump.sql "https://s3.amazonaws.com/intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql"

# remove db and user creations
for i in {1..10}
do
    sed -i '18d' 7-dump.sql
done

# change use statement
sed -i 's/_dev/_test/' 7-dump.sql

# import mysqldump 
cat 7-dump.sql | mysql -uhbnb_test -phbnb_test_pwd

# cleanup
rm 7-dump.sql