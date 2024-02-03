-- Prepares MYSQL server for the project

-- Create database for testing
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create a new user for testing
CREATE USER
       IF NOT EXISTS 'hbnb_test'@'localhost'
       IDENTIFIED BY 'hbnb_test_pwd';

GRANT ALL ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT on performance_schema.* TO 'hbnb_test'@'localhost';
