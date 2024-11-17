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
  name varchar(255) NOT NULL
);

CREATE TABLE users (
    uid varchar(255) NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL,
    mailaddress varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    sex varchar(30) NOT NULL,
    sharehouseid int NOT NULL REFERENCES sharehouse(id),
    comment varchar(255),
    admin boolean 
);

CREATE TABLE statuses (
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(255)
);

CREATE TABLE chatgroups (
    cid int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    required int NOT NULL,
    comment varchar(255),
    statusid int REFERENCES statuses(id)
);

CREATE TABLE usergroups (
    user_id varchar(255) NOT NULL REFERENCES users(uid),
    group_id int NOT NULL REFERENCES chatgroups(cid)
);

CREATE TABLE messages (
    mid int PRIMARY KEY AUTO_INCREMENT,
    user_id varchar(255)  NOT NULL REFERENCES users(uid),
    group_id int REFERENCES chatgroups(cid),
    creatdate date not null,
    message varchar(255)
);

-- サンプルユーザーをINSERT
INSERT INTO users(uid, name, mailaddress, password,sex,sharehouseid)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','ねむ太郎','sasuganinemui@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578','man',1);
INSERT INTO chatgroups(cid, name, required, comment, statusid)VALUES(1,'バスケグループ',0,'0',0);