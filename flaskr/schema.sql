SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Profiles;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Persons;
SET FOREIGN_KEY_CHECKS=1;
CREATE TABLE Persons (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255)
);
CREATE TABLE Users (
    id int AUTO_INCREMENT,
    username varchar(20) NOT NULL,
    password varchar(32) NOT NULL,
    nickname varchar(20) NOT NULL,
    email varchar(20) NOT NULL,
    country varchar(30) NOT NULL,
    sign_up_date DATETIME NOT NULL,	
    last_login DATETIME, 
    PRIMARY KEY(id), 
    UNIQUE(id),
    UNIQUE(username)
);
CREATE TABLE Profiles (
    user_id int NOT NULL, 
    bio MEDIUMTEXT DEFAULT '',
    locations MEDIUMTEXT DEFAULT '',
    ratings int DEFAULT 0 NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
CREATE TABLE Reviews( 
    review_id int AUTO_INCREMENT, 
    reviewer_id int NOT NULL,
    reviewed_id int NOT NULL, 
    body MEDIUMTEXT NOT NULL, 
    rating int NOT NULL,
    PRIMARY KEY (review_id)
);
