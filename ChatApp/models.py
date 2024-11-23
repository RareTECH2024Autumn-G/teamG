# 2024/11/15追加
# おそらくSQLのテンプレート。実行する時にここを呼び出せるようにする
# 2024/11/16tara追加
# createUser, getUseを修正,idはPythonの組み込み関数や名前 (id や list など) とかぶってしまうので、uidに変更
# init.sql 修正（idはPythonの組み込み関数や名前 (id や list など) とかぶってしまうのでuid等に変更、uid passwordはハッシュ化やUUIDを使用する関係で変更）
# init.sql 修正（AUTO_INCREMENT削除、UUIDにて作成するため, uid int→varcharに変更,varchar(50)→varchar(255)に修正）
# login.html 修正（名前ではなく、メールアドレスで認証させる）


import pymysql
from flask import abort
from util.DB import DB


class dbConnect:
    @staticmethod
    def createUser(uid, name, mailaddress, password,sex,sharehouse_id,firstlogin):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO users (uid, name, mailaddress, password,sex,sharehouse_id,firstlogin) VALUES (%s, %s, %s, %s,%s,%s,%s);'
            cur.execute(sql, (uid, name, mailaddress, password,sex,sharehouse_id,firstlogin))
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod
    def getUser(mailaddress): 
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT * FROM users WHERE mailaddress=%s;'
            cur.execute(sql, (mailaddress))
            user = cur.fetchone()
            return user
        except (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #20241118 うっちゃん 1回目のログインかを判別する
    def checkfirst(mailaddress):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT firstlogin FROM users WHERE mailaddress=%s;'
            cur.execute(sql, (mailaddress,))
            firstlogin = cur.fetchone()
            # print(f"models.py 57 DEBUG: checkfirst(mailaddress) = {firstlogin}")  # 戻り値を出力
            return firstlogin
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #20241120 うっちゃん 選択したサービスを保存する
    def registgroups(user_id,selectgroups):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO usergroups (user_id, group_id) VALUES (%s, %s);'

            selectgroup = 1
            for selectgroup in selectgroups:
                cur.execute(
                    sql,(user_id,selectgroup)
                )
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #20241120 うっちゃん 必須グループを登録
    def registrequiregroups(uid, sexcid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            
            #必須グループの1つ目の登録
            allcid = 1  
            sql = 'INSERT INTO usergroups (user_id, group_id) VALUES (%s, %s);'
            cur.execute(sql,(uid,allcid))

            # 必須グループ2つ目の登録
            cur.execute(sql, (uid, sexcid))            
            
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #20241122 うっちゃん ユーザーデータが存在するか確認する
    def checkfirstuser(user_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT firstlogin FROM users WHERE uid=%s;'
            cur.execute(sql, (user_id))
            user = cur.fetchone()
            return user
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #20241120 うっちゃん 初回ログインフラグを更新する
    def updatefirstlogin(user_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'UPDATE users SET firstlogin = 0 WHERE uid=%s;'
            cur.execute(sql, (user_id))
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()
 
    @staticmethod # 2024/11/21 うっちゃん 所属しているグループをusergroupsから取得する
    def getbelonggroups(user_id): 
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT group_id,name FROM usergroups INNER JOIN chatgroups ON cid = group_id WHERE user_id=%s;'
            cur.execute(sql, (user_id))
            getgroupsall = cur.fetchall()
            return getgroupsall
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    @staticmethod
    def getallgroups(user_id): # 2024/11/21　うっちゃん所属していないグループを全表示する
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT group_id,name FROM usergroups INNER JOIN chatgroups ON cid = group_id WHERE user_id<>%s;'
            # 複数グループを取れるようにする
            # 自分が所属しているテーブルを取ってから除外する？？？？
            cur.execute(sql, (user_id))
            groups = cur.fetchone()
            print(f"models.py170 DEBUG: 存在していないグループ = {groups}")  # 戻り値を出力
            return groups
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    # def getChannelById(cid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'SELECT * FROM channels WHERE id=%s;'
    #         cur.execute(sql, (cid))
    #         channel = cur.fetchone()
    #         return channel
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def getChannelByName(channel_name):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'SELECT * FROM channels WHERE name=%s;'
    #         cur.execute(sql, (channel_name))
    #         channel = cur.fetchone()
    #         return channel
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def addChannel(uid, newChannelName, newChannelDescription):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);'
    #         cur.execute(sql, (uid, newChannelName, newChannelDescription))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def getChannelByName(channel_name):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'SELECT * FROM channels WHERE name=%s;'
    #         cur.execute(sql, (channel_name))
    #         channel = cur.fetchone()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()
    #         return channel


    # def updateChannel(uid, newChannelName, newChannelDescription, cid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;'
    #         cur.execute(sql, (uid, newChannelName, newChannelDescription, cid))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # #deleteチャンネル関数
    # def deleteChannel(cid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'DELETE FROM channels WHERE id=%s;'
    #         cur.execute(sql, (cid))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def getMessageAll(cid):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;'
    #         cur.execute(sql, (cid))
    #         messages = cur.fetchall()
    #         return messages
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def createMessage(uid, cid, message):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)'
    #         cur.execute(sql, (uid, cid, message))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


    # def deleteMessage(message_id):
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'DELETE FROM messages WHERE id=%s;'
    #         cur.execute(sql, (message_id))
    #         conn.commit()
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()

# 2024/11/23 yoneyama add start
    def getGroup(groupname):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT c.cid ,c.name ,c.required ,c.comment ,c.statusid FROM chatgroups c WHERE c.name = %s;"
            cur.execute(sql, (groupname))
            group = cur.fetchone()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
            return group

    def getMessage(group_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT m.mid ,m.user_id ,m.group_id ,m.creatdate ,m.message FROM messages m WHERE m.group_id = %s;"
            cur.execute(sql, (group_id))
            messages = cur.fetchone()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
            return messages

    def createMessage(i_user_id , i_group_id , l_datetime , l_message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(user_id , group_id , createdate ,message)VALUES(%s ,%s ,%s ,%s);"
            cur.execute(sql, (i_user_id , i_group_id , l_datetime , l_message))
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
# 2024/11/23 yoneyama add end
