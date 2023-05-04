-- create a database name hbnb_test_db
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- drops user if database exists
-- DROP USER IF EXISTS 'hbnb_test'@'localhost';
-- creates a user with user:hbnb_test@localhost with pass hbnb_test_pwd
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost'IDENTIFIED BY 'hbnb_test_pwd';
-- if user root@localhost unable to grant priv
-- http://stackoverflow.com/questions/21714869/error-1044-42000-access-denied-for-root-with-all-privileges
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- grant user hbnb_test all privileges to database hbnb_test_db
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
