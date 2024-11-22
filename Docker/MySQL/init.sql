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

CREATE TABLE sharehouses (
    sid int NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 2024/11/20 うっちゃん更新
    name varchar(255) NOT NULL
);

CREATE TABLE users (
    uid varchar(255) NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL,
    mailaddress varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    sex varchar(30) NOT NULL,
    sharehouse_id int NOT NULL REFERENCES sharehouse(sid),
    comment varchar(255),
    admin boolean,
    firstlogin int-- 2024118 うっちゃん firstloginを追加
);

CREATE TABLE statuses (
    stid int NOT NULL PRIMARY KEY AUTO_INCREMENT,-- 2024/11/20 うっちゃん更新
    name varchar(50)-- 2024/11/20 うっちゃん更新
);

CREATE TABLE chatgroups (
    cid int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    required int NOT NULL,
    comment varchar(255),
    status_id int REFERENCES statuses(stid) -- 2024/11/20 うっちゃん更新（今後NotNull制約を付与する）
);

CREATE TABLE usergroups (
    user_id varchar(255) NOT NULL REFERENCES users(uid),
    group_id int NOT NULL REFERENCES chatgroups(cid)
);

CREATE TABLE messages (
    mid int PRIMARY KEY AUTO_INCREMENT, -- 2024/11/20 うっちゃん更新（今後NotNull制約を付与する）
    user_id varchar(255)  NOT NULL REFERENCES users(uid),
    group_id int REFERENCES chatgroups(cid),
    creatdate date not null,
    message varchar(255)
);

-- サンプルユーザーをINSERT
INSERT INTO users(uid, name, mailaddress, password,sex,sharehouse_id)VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','ねむ太郎','sasuganinemui@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578','man',1);

-- 2024/11/18 初期表示のグループ6こをINSERT
INSERT INTO chatgroups(cid, name, required, comment, status_id)VALUES
-- 2024/11/22 全体・男性・女性の基本グループを追加　うっちゃん
(1,'シェアハウス全体グループ',0,'全体へのイベントはここで告知してください',0),
(2,'男性フロア連絡グループ',0,'男性フロアへの周知事項はここでおこなってください',0),
(3,'女性フロア連絡グループ',0,'女性フロアへの周知事項はここでおこなってください',0),
(4,'バスケグループ',0,'初心者大歓迎！バスケを週末にやってます。',0),
(5,'野球グループ',0,'草野球です',0),
(6,'音楽グループ',0,'一緒に歌いましょう',0),
(7,'ドッチボールグループ',0,'童心に還る',0),
(8,'お茶グループ',0,'chillしよ〜〜〜',0),
(9,'モルックグループ',0,'レアスポーツを楽しみましょう！',0);