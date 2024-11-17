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
    def createUser(uid, name, mailaddress, password,sex,sharehouseid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO users (uid, name, mailaddress, password,sex,sharehouseid) VALUES (%s, %s, %s, %s,%s,%s);'
            cur.execute(sql, (uid, name, mailaddress, password,sex,sharehouseid))
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


    # def getChannelAll():
    #     try:
    #         conn = DB.getConnection()
    #         cur = conn.cursor()
    #         sql = 'SELECT * FROM channels;'
    #         cur.execute(sql)
    #         channels = cur.fetchall()
    #         return channels
    #     except Exception as e:
    #         print(f'エラーが発生しています：{e}')
    #         abort(500)
    #     finally:
    #         cur.close()


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
