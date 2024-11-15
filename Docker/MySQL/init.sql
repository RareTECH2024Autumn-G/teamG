-- DROP DATABASE chatapp;
-- DROP USER 'testuser';

-- CREATE USER 'testuser' IDENTIFIED BY 'testuser';
-- CREATE DATABASE sharehappy;
-- USE sharehappy
-- GRANT ALL PRIVILEGES ON sharehappy.* TO 'testuser';

-- 11/15/05:00 DB接続
DROP DATABASE IF EXISTS sharehappy;
DROP USER IF EXISTS 'testuser';

CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';
CREATE DATABASE IF NOT EXISTS sharehappy;
USE sharehappy;

GRANT ALL PRIVILEGES ON sharehappy.* TO 'testuser'@'%';
FLUSH PRIVILEGES;
-- end 11/15/05:00 DB接続

CREATE TABLE sharehouse (
  id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name varchar(50) NOT NULL
);

CREATE TABLE users (
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    mailaddress varchar(50) NOT NULL,
    password varchar(50) NOT NULL,
    sex int NOT NULL,
    sharehouseid int NOT NULL REFERENCES sharehouse(id),
    comment varchar(255),
    admin boolean 
);

CREATE TABLE statuses (
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(50)
);

CREATE TABLE chatgroups (
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    required int NOT NULL,
    comment varchar(255),
    statusid int REFERENCES status(id)
);

CREATE TABLE usergroups (
    user_id int NOT NULL REFERENCES users(id),
    group_id int NOT NULL REFERENCES chatgroups(id)
);

CREATE TABLE messages (
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int REFERENCES users(id),
    group_id int REFERENCES chatgroups(id),
    creatdate date not null,
    message varchar(255)
);

-- サンプルユーザーをINSERT
INSERT INTO users(id, name, mailaddress, password)VALUES(1,'ねむ太郎','sasuganinemui@gmail.com','netaina');
