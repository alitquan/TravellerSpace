DROP TABLE IF EXISTS Persons; 
DROP TABLE IF EXISTS Users;
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
    UNIQUE(id),
    UNIQUE(username)
);
