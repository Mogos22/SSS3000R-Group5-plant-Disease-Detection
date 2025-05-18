--create the database

CREATE DATABASE IF NOT EXISTS plant_disease_detection;

--use the database
use plant_disease_detection;

--create the tomato table
CREATE TABLE IF NOT EXISTS tomato (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    point_in_time DATETIME,
    dato TEXT,
    detected_disease VARCHAR(255),
    image varchar(255)	

);


--create the tomato table
CREATE TABLE IF NOT EXISTS apple (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    point_in_time DATETIME,
    dato TEXT,
    detected_disease VARCHAR(255),
    image varchar(255)	

);
