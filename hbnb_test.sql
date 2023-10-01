-- Create the database if it doesn't exist
DROP DATABASE IF EXISTS hbnb_test_db;
CREATE DATABASE hbnb_test_db;

-- Use the newly created database
USE hbnb_test_db;

-- Create the tables
CREATE TABLE states (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE cities (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(128) NOT NULL,
    state_id VARCHAR(60) NOT NULL,
    FOREIGN KEY (state_id) REFERENCES states (id)
);

CREATE TABLE users (
    email VARCHAR(128) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE amenities (
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE places (
    city_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(1024),
    number_rooms INT NOT NULL DEFAULT 0,
    number_bathrooms INT NOT NULL DEFAULT 0,
    max_guest INT NOT NULL DEFAULT 0,
    price_by_night INT NOT NULL DEFAULT 0,
    latitude FLOAT,
    longitude FLOAT,
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE reviews (
    text VARCHAR(1024) NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    id VARCHAR(60) NOT NULL PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE place_amenity (
    place_id VARCHAR(60) NOT NULL,
    amenity_id VARCHAR(60) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Insert mock data into amenities table
INSERT INTO amenities (id, name) VALUES
    ('1', 'Wi-Fi'),
    ('2', 'TV'),
    ('3', 'Air Conditioning');

-- Insert mock data into states table
INSERT INTO states (id, name) VALUES
    ('CA', 'California'),
    ('NY', 'New York'),
    ('TX', 'Texas');

-- Insert mock data into cities table
INSERT INTO cities (id, state_id, name) VALUES
    ('101', 'CA', 'Los Angeles'),
    ('102', 'CA', 'San Francisco'),
    ('201', 'NY', 'New York City');

-- Insert mock data into users table
INSERT INTO users (email, password, first_name, last_name, id) VALUES
    ('user1@example.com', 'password1', 'John', 'Doe', '1001'),
    ('user2@example.com', 'password2', 'Jane', 'Smith', '1002'),
    ('user3@example.com', 'password3', 'Alice', 'Johnson', '1003');

-- Insert mock data into places table
INSERT INTO places (city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, id) VALUES
    ('101', '1001', 'Cozy Apartment', 'A cozy apartment in the heart of the city.', 2, 1, 4, 100, 34.0522, -118.2437, '2001'),
    ('102', '1002', 'Luxury Penthouse', 'A luxurious penthouse with stunning views.', 3, 2, 6, 300, 37.7749, -122.4194, '2002'),
    ('201', '1003', 'Charming Studio', 'A charming studio apartment in downtown.', 1, 1, 2, 80, 40.7128, -74.0060, '2003');

-- Insert mock data into reviews table
INSERT INTO reviews (text, place_id, user_id, id) VALUES
    ('Great place to stay!', '2001', '1001', '3001'),
    ('Awesome view from the penthouse.', '2002', '1002', '3002'),
    ('Perfect location for exploring the city.', '2003', '1003', '3003');

-- Insert mock data into place_amenity table (relating amenities to places)
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('2001', '1'),
    ('2001', '2'),
    ('2002', '1'),
    ('2002', '3'),
    ('2003', '2');
