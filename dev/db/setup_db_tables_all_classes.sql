-- creates MySQL database hbnb_dev_db only if not existing
-- and gives privileges to user hbnb_dev on 2 DB's
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.*
      TO hbnb_dev@localhost
      IDENTIFIED BY 'hbnb_dev_pwd';
GRANT SELECT ON performance_schema.*
      TO hbnb_dev@localhost
      IDENTIFIED BY 'hbnb_dev_pwd';
-- additions to attempt to pass last assignment
USE hbnb_dev_db;
CREATE TABLE states
       (id varchar(60) NOT NULL UNIQUE,
       created_at DATETIME(6),
       updated_at DATETIME(6),
       name varchar(128) NOT NULL,
       PRIMARY KEY (id));
CREATE TABLE cities
       (id varchar(60) NOT NULL UNIQUE,
       created_at DATETIME(6),
       updated_at DATETIME(6),
       name varchar(128) NOT NULL,
       state_id varchar(60),
       FOREIGN KEY (state_id) REFERENCES states(id),
       PRIMARY KEY (id));
CREATE TABLE users
       (id varchar(60) NOT NULL UNIQUE,
       created_at DATETIME(6),
       updated_at DATETIME(6),
       email varchar(128) NOT NULL,
       password varchar(128) NOT NULL,
       first_name varchar(128),
       last_name varchar(128),
       PRIMARY KEY (id));
CREATE TABLE amenities
       (id varchar(60) NOT NULL UNIQUE,
       created_at DATETIME(6),
       updated_at DATETIME(6),
       name varchar(128) NOT NULL,
       PRIMARY KEY (id));
CREATE TABLE places
       (id varchar(60) NOT NULL UNIQUE,
       created_at DATETIME(6),
       updated_at DATETIME(6),
       name varchar(128) NOT NULL,
       city_id varchar(60) NOT NULL,
       user_id varchar(60) NOT NULL,
       description varchar(1024),
       number_rooms int NOT NULL DEFAULT 0,
       number_bathrooms int NOT NULL DEFAULT 0,
       max_guest int NOT NULL DEFAULT 0,
       price_by_night int NOT NULL DEFAULT 0,
       latitude float,
       longitude float,
       FOREIGN KEY (city_id) REFERENCES cities(id),
       FOREIGN KEY (user_id) REFERENCES users(id),
       PRIMARY KEY (id));
CREATE TABLE place_amenity
       (id int NOT NULL AUTO_INCREMENT,
       place_id varchar(60) NOT NULL,
       amenity_id varchar(60) NOT NULL,
       FOREIGN KEY (place_id) REFERENCES places(id),
       FOREIGN KEY (amenity_id) REFERENCES amenities(id),
       PRIMARY KEY (id));
