-- create a database name hbnb_dev_db
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- drops user if database exists
-- DROP USER IF EXISTS 'hbnb_dev'@'localhost';
-- creates a user with user:hbnb_dev@localhost with pass hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost'IDENTIFIED BY 'hbnb_dev_pwd';
-- if user root@localhost unable to grant priv
-- http://stackoverflow.com/questions/21714869/error-1044-42000-access-denied-for-root-with-all-privileges
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- grant user hbnb_dev all privileges to database hbnb_dev_db
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
