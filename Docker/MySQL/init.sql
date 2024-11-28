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
    sharehouse_id int NOT NULL REFERENCES sharehouses(sid),
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
    createdate date not null,
    message varchar(255)
);

-- サンプルユーザーをINSERT-- 2024/11/23 タラ追記（サンプルユーザー追加）
INSERT INTO users(uid, name, mailaddress, password,sex,sharehouse_id)VALUES
('970af84c-dd40-47ff-af23-282b72b7cca8','ねむ太郎','sasuganinemui@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578','man',1),
('c58a7b1d-1e75-48cb-bf19-4e3d5f9e8e9f', '睡眠次郎', 'suiminjiro@gmail.com', 'e8d5c8240b1b8ed2a6f6c94701c5b83cfad67f07c1d6889c08b5c23660d8723e', 'man', 1),
('d4a7c3bb-19d6-41c5-8f3f-8dcf0e48f154', 'いねむり花子', 'inemurihanako@gmail.com', 'b1c51e77de84c1f8a4e68429c223ea7e81e43bda0154d857cba8cbded17fb2f1', 'woman', 1),
('32b4a7d9-2e44-4d38-bc55-91e2d8e556d7', 'ねむりの小五郎', 'nemurino.kogoro@gmail.com', 'c7e8d8f6b4c4d8e7a6b7c98705c6d57b9a8367f13cbd8d7c12c7a4d0172c8e64', 'man', 1),
('94d3f2a7-2c56-4fb9-a8e4-fcda4d6b83e4', 'ねむり姫', 'nemurihime@gmail.com', 'd1c34a76fe85b2e7a5c6c8e709d5b93e78d67f12d0a678c71c8b4d25d2f9c867', 'woman', 1),
('a2c9e7d4-5e31-4fd2-9b8c-6e4d9a6f81c2', 'スリープ一郎', 'sleepichiro@gmail.com', 'f3d74a96fe85d3e7a9c6c8d708c5d63e85b57f12d4a698c83c7b5d45e1c9d876', 'man', 1);


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

-- 2024/11/28 初期表示のメッセージをINSERT
INSERT INTO messages(mid, user_id, group_id, createdate, message)VALUES
(1,'970af84c-dd40-47ff-af23-282b72b7cca8',1,'2024/11/28','初めてのコメントです'),
(2,'970af84c-dd40-47ff-af23-282b72b7cca8',1,'2024/11/28','みなさん初めまして'),
(3,'970af84c-dd40-47ff-af23-282b72b7cca8',3,'2024/11/28','初めてのコメントです');
