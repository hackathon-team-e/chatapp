import pymysql

class Db:
    def getConnection():
        try:
            conn = pymysql.connect(
            host="localhost",
            db="chatapp",
            user="testuser",
            password="Testuser1!",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
            return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()
