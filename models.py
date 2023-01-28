from util.db import DB

class dbConnect:

    # チャンネル一覧を取得
    def getChannelAll():
            try:
                conn = DB.getConnection()
                cur = conn.cursor()
                sql = "SELECT * FROM channels;"
                cur.execute(sql)
                channels = cur.fetchall()
                return channels
            except Exception as e:
                print(e + 'が発生しています')
                return None
            finally:
                cur.close()

    # チャンネル名を取得
    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # チャンネルを追加
    def addChannel(newChannelName, newChannelDescription):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (name, abstract) VALUES (%s, %s, %s);"
            cur.execute(sql, (newChannelName, newChannelDescription))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # チャンネル情報を更新
    def updateChannel(newChannelName, newChannelDescription, cid):
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "UPDATE channels SET name=%s, abstract=%s WHERE id=%s;"
        cur.execute(sql, (newChannelName, newChannelDescription, cid))
        conn.commit()
        cur.close()

    # チャンネルIDを取得
    def getChannelById(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # メッセージ一覧を取得
    def getMessageAll(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT id,u.uid, user_name, message FROM messages AS m INNER JOIN users AS u ON m.uid = u.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # チャンネル削除
    def deleteChannel(cid):
        try: 
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()
