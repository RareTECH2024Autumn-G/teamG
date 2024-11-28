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

    @staticmethod #20241120 うっちゃん 選択したサービスを保存する(新規グループ追加、既存グループ参加で使用)
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
            sql = '''
                SELECT cg.cid, cg.name 
                FROM chatgroups cg 
                LEFT JOIN ( 
                SELECT ug.group_id 
                FROM usergroups ug 
                INNER JOIN chatgroups cg_inner ON ug.group_id = cg_inner.cid 
                WHERE ug.user_id = %s 
                ) subquery ON cg.cid = subquery.group_id 
                WHERE subquery.group_id IS NULL AND cg.cid>3;
                '''
            cur.execute(sql, (user_id))
            groups = cur.fetchall() #複数グループを取得
            print(f"models.py177 DEBUG: 取得できたグループ = {groups}")  # 戻り値を出力
            return groups
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
    
    @staticmethod# 2024/11/23 タラ追記（ユーザー一覧を取得）    
    def getallusers(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT uid,name FROM users WHERE uid<>%s;'
            # 自分以外の複数usersを取れるようにする
            cur.execute(sql, (uid,))
            users = cur.fetchall()
            print(f"models.py182 DEBUG: users = {users}")  # 戻り値を出力
            return users
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()

    @staticmethod# 2024/11/23 タラ追記（新しいchatgroupsを追加）    
    def createGroup(name,required,comment):
        try:
            status_id = 0
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO chatgroups (name,required,comment,status_id) VALUES (%s, %s, %s, %s);'
            cur.execute(sql,(name,required,comment,status_id))
            conn.commit()
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT cid FROM chatgroups WHERE name=%s;'
            cur.execute(sql, (name))
            cid = cur.fetchone()
            print(f"models.py207 DEBUG: cid = {cid}")  # 戻り値を出力
            return cid
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()
    
    @staticmethod# 2024/11/23 タラ追記（usergruopsに新しいgroup_idを追加する）    
    def addGroup(selectUsers, cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO usergroups (user_id, group_id) VALUES (%s, %s);'
            print(f"DEBUG: selectUsersの型: {type(selectUsers)} 値: {selectUsers}")
            for selectUser in selectUsers:
                cur.execute(
                    sql,(selectUser,cid['cid'])
                )
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #2024/11/24 うっちゃん user情報を取得する    
    def getuserinfo(user_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT * FROM users WHERE uid = %s;'
            cur.execute(sql, (user_id))
            getuserinfo = cur.fetchone()
            print(f'models.py254 DEBUG: ユーザー情報 = {getuserinfo}') 
            return getuserinfo
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()

    @staticmethod #2024/11/24 うっちゃん user情報を更新する    
    def updateuserinfo(user_id, name, mailaddress, password, sharehouse_id,comment):
        print(f"DEBUG: uid={user_id}, name={name}, mailaddress={mailaddress}, password={password}, sharehouse_id={sharehouse_id}")
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'UPDATE users SET name = %s ,mailaddress = %s ,password = %s , sharehouse_id = %s ,comment = %s WHERE uid = %s;'
            cur.execute(sql, (name,mailaddress,password,sharehouse_id,comment,user_id))
            conn.commit()
        except  (pymysql.DatabaseError, pymysql.OperationalError)  as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            # curが定義されている場合のみcloseする
            if 'cur' in locals() and cur is not None:
                cur.close()
      
# 2024/11/23 yoneyama add start
    def getGroup(groupname):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()

            sql = "SELECT c.cid as id ,c.name as name ,c.comment as abstract FROM chatgroups c WHERE c.name = %s;"
            cur.execute(sql, (groupname))
            group = cur.fetchone()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
            return group

    def getMessage(groupname):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()

            sql = '''
            SELECT m.mid as id ,m.user_id as user_id ,m.createdate as created_at ,m.message as content ,u.name as user_name 
            FROM messages m INNER JOIN users AS u ON m.user_id = u.uid 
            INNER JOIN chatgroups g ON m.group_id = g.cid WHERE g.name = %s;
            '''
            cur.execute(sql, (groupname))
            messages = cur.fetchall()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
            return messages


        #yoneyamaさん 11/28 
#         def getMessage(groupname):
#         try:
#             conn = DB.getConnection()
#             cur = conn.cursor()
# #            sql = "SELECT m.mid ,m.user_id ,m.group_id ,m.creatdate ,m.message FROM messages m WHERE m.group_id = %s;"
# #            sql = "SELECT m.mid as id ,m.user_id as user_id ,m.creatdate as created_at ,m.message as content ,u.name as user_name FROM messages m INNER JOIN users AS u ON m.user_id = u.uid INNER JOIN chatgroups g ON m.group_id = g.cid WHERE g.name = %s;"
# #            sql = "SELECT u.name as user_name , m.creatdate as created_at ,m.message as content FROM messages m INNER JOIN users AS u ON m.user_id = u.uid INNER JOIN chatgroups g ON m.group_id = g.cid WHERE g.name = %s;"
#             sql = "SELECT m.creatdate as created_at ,m.message as content 
#             FROM messages m INNER JOIN users AS u ON m.user_id = u.uid 
#             INNER JOIN chatgroups g ON m.group_id = g.cid WHERE g.name = %s;"
#             cur.execute(sql, (groupname))
#             messages = cur.fetchone()
#         except Exception as e:
#             print(f'エラーが発生しています：{e}')
#             abort(500)
#         finally:
#             cur.close()
#             return messages

    def createMessage(i_user_id , i_group_id , l_datetime , l_message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(user_id , group_id , createdate ,message)VALUES(%s ,%s ,%s ,%s);"
            cur.execute(sql, (i_user_id , i_group_id , l_datetime , l_message))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            cur.close()
# 2024/11/23 yoneyama add end
