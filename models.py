
class dbConnect:
    def createMessage(uid, cid, message):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"#INSERT INTOはデータの新規登録する際に使用される messagesはテーブル名()の中は登録するカラム名でVALUEの後ろは登録するデータ
            cur.execute(sql,(uid, cid, message)) #execute は一連のターゲットに対してSQLコマンドを実行
            conn.comimit() #トランザクションで仮だったものが確定しデータベースに結果が反映されトランザクションが終了 一度コミットすると、もう処理を取り消してデータをもとに戻すことができない
        except Exception as e:#Exceptionはシステム終了以外の例外基底クラスのこと。システム終了以外の全てのエラーをキャッチする
            print(e +'が発生しています')
            return None
        finally: #例外が発生してもしなくても最後に実行する処理のこと
            cur.close()


    def deleteMessage(message_id):
        try:
            conn = DB.getConection()
            cur = conn.cursor()
            sql ="DELETE FROM messages WHERE id=%s;" #DELETEはテーブルを削除する messagesのテーブルからid=%sのものを削除するという命令 %s %はLIKE演算子 任意数 (0 文字を含む) の連続した文字に相当 sは文字列を意味
            cur.execute(sql(message_id))
            conn.comit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
            cur.close()