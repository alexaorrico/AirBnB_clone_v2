create database if not exists hbnb_test_db;
create user if not exists 'hbnb_test'@'localhost' identified by 'hbnb_test_pwd';
grant all on hbnb_test_db.* to 'hbnb_test'@'localhost';
grant select on performance_schema.* to 'hbnb_test'@'localhost';
