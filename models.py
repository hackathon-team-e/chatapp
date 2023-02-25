from util.db import Db

class DbConnect:

    # ユーザー登録処理
    def createUser(user):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (user_id, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (user.user_id, user.user_name, user.email, user.password))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # emailからユーザーを取得
    def getUserByEmail(email):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close


    # user_nameからユーザーを取得
    def getUserByName(user_name):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE user_name=%s;"
            cur.execute(sql, (user_name))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close


    # user_name or emailでユーザーを取得
    def getRegisteredUser(user_name, email):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE user_name=%s OR email=%s;"
            cur.execute(sql, (user_name, email))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close


    # チャンネル一覧を取得
    def getChannelAll(user_id):
            try:
                conn = Db.getConnection()
                cur = conn.cursor()
                sql = "SELECT * FROM channels AS c INNER JOIN channel_users AS cu ON c.channel_id = cu.channel_id WHERE cu.user_id=%s;"
                cur.execute(sql, (user_id))
                channels = cur.fetchall()
                return channels
            except Exception as e:
                print(e + 'が発生しています')
                return None
            finally:
                cur.close()


    # チャンネルをchannel_nameから取得
    def getChannelByName(channel_name):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE channel_name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # チャンネルをchannel_idから取得
    def getChannelById(channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE channel_id=%s;"
            cur.execute(sql, (channel_id))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # チャンネルIDを取得
    def getChannelId(user_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT channel_id FROM channel_users WHERE user_id=%s;"
            cur.execute(sql, (user_id))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # チャンネルを追加
    def addChannel(user_id, newChannelName, newChannelDescription):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (user_id, channel_name, abstract) VALUES (%s, %s, %s);"
            cur.execute(sql, (user_id, newChannelName, newChannelDescription))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()

    # チャンネルにユーザーを追加
    def addChannelUser(user_id, channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channel_users (user_id, channel_id) VALUES (%s, %s);"
            cur.execute(sql, (user_id, channel_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # チャンネル情報を更新
    def updateChannel(user_id, newChannelName, newChannelDescription, channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels SET user_id=%s, channel_name=%s, abstract=%s WHERE channel_id=%s;"
            cur.execute(sql, (user_id, newChannelName, newChannelDescription, channel_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
        finally:
            cur.close()


    # チャンネル削除
    def deleteChannel(channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE channel_id=%s;"
            cur.execute(sql, (channel_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # メッセージ一覧を取得
    def getMessageAll(channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT m.message_id, m.user_id, m.message, u.user_name FROM messages AS m INNER JOIN users AS u ON m.user_id = u.user_id WHERE channel_id = %s ORDER BY m.created_at ASC;"
            cur.execute(sql, (channel_id))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # 新規メッセージを登録
    def createMessage(user_id, channel_id, message):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(user_id, channel_id, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (user_id, channel_id, message))
            conn.commit()
        except Exception as e:
            print(e +'が発生しています')
            return None
        finally:
            cur.close()


    # メッセージ削除処理
    def deleteMessage(message_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE message_id=%s;"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # ユーザー情報を取得
    def getUserDetail(user_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            user_id = str(user_id)
            sql = "SELECT user_name,email FROM users WHERE user_id=%s;"
            cur.execute(sql,(user_id))
            userDetail = cur.fetchone()
            return userDetail
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()


    # チャンネルのユーザーを取得
    def getChannelUser(user_id, channel_id):
        try:
            conn = Db.getConnection()
            cur = conn.cursor()
            sql = "SELECT user_id FROM channel_users WHERE user_id=%s AND channel_id=%s;"
            cur.execute(sql,(user_id, channel_id))
            user_id = cur.fetchone()
            return user_id
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()