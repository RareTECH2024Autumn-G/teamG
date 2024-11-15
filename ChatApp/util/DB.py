import pymysql

class DB:
    def getConnection():
        try:
            conn = pymysql.connect(
            host="db",
            db="sharehappy",
            user="testuser",
            password="testuser",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
            return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()
