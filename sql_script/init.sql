CREATE DATABASE taxi_booker;

USE taxi_booker;

CREATE TABLE taxi_position (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    taxi_id VARCHAR(8) NOT NULL UNIQUE,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8)
);