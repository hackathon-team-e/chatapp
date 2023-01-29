
from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect
# from util.user import User
# from datetime import timedelta
# import hashlib
# import uuid
# import re

app = Flask(__name__)

# チャンネル一覧
@app.route('/')
def index():
    # uid = session.get("uid")
    # if uid is None:
    #     return redirect('/login')
    # else:
    channels = dbConnect.getChannelAll()
    return render_template('index.html', channels=channels)

# チャンネル作成
@app.route('/', methods=['POST'])
def add_channel():
    # uid = session.get('uid')
    # if uid is None:
    #     return redirect('/login')
    channel_name = request.form.get('channel-title')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channel-description')
        dbConnect.addChannel(channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

# チャンネル編集
app.route('/update_channel', methods=['POST'])
def update_channel():
    # uid = session.get("uid")
    # if uid is None:
    #     return redirect('/login')

    cid = request.form.get('cid')
    channel_name = request.form.get('channel-title')
    channel_description = request.form.get('channel-description')

    dbConnect.updateChannel(channel_name, channel_description, cid)
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    return render_template('detail.html', messages=messages, channel=channel)


# チャンネル削除
# uidもmessageと一緒に返す
@app.route('/detail/<cid>')
def detail(cid):
    # uid = session.get("uid")
    # if uid is None:
    #     return redirect('/login')
    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)

    return render_template('detail.html', messages=messages, channel=channel)


#＜メッセージ一覧機能＞ メッセージ追加も削除もされてない最初にチャットを開いた時の状態  詳細
@app.route('/detail/<cid>')
def detail(cid):
    # uid =session.get("uid")
    # if uid is None:
    #     return redirect('/login')
    cid = cid
    channel =dbConnect.getChannelById(cid)
    messages =dbConnect.getMessageAll(cid)
    
    return render_template('detail.html',messages=messages, channel=channel)


#＜メッセージの作成機能＞
#メッセージを送った時に裏でされている処理 uidを取ってきて、あったらメッセージとid(これは見えないけど、その部屋にメッセージを送るという意味)を表示する
@app.route('/message', methods=['POST'])#messageのページにいったときにPOST（URLに含めない形）でデータを送ってねって処理
def add_message():#messegeを送ったら（送信ボタン押したら）messegeページに移動する関数
    # uid = session.get("uid")
    # if uid is None:
    #     return redirect('/login')#sessionでuidを取ってくるけど、もしなかったらloginページに移動しろ

    message = request.form.get('message')#htmlのdetalilからmessageを持ってきて、message変数に代入
    channel_id = request.form.get('channel_id')#htmlのdetalilからchannel_idを持ってきて、channel_id変数に代入

    if message:
        dbConnect.createMessage(channel_id, message)#もしdbConectの中にある、createMessageの中にある、uid,channel_id,messageだったら↓

    channel =dbConnect.getChannelById(channel_id)#もし上の処理がtrueなら、dbConectのgetChannelByIdからchannel_idを持ってきて、channel変数に代入する
    messages =dbConnect.getMessageAll(channel_id)#もし上の処理がtrueなら、dbConectのgetMessageAllからchannel_idを持ってきて、messages変数に代入する

    return render_template('detail.html',messages=messages, channel=channel)#？？？？html以外の引数はよく分からない？？？？




#＜メッセージの削除機能＞
@app.route('/delete_message', methods=['POST'])
def delete_message():
    # uid = session.get("uid")
    # if uid is None:
    #     return redirect('/login')#メッセージ作成時と同様の処理  sessionでuidを取ってくるけど、もしなかったらloginページに移動しろ
    
    message_id = request.form.get('message_id')#detail.htmlのinputタグのnameがmessage_idのところからとってきている
    cid =request.form.get('channel_id')#detail.htmlのinputタグのnameがchannle_idのところからとってきている
    if message_id :
        dbConnect.deleteMessage(message_id)

    channle =dbConnect.getChannelById(cid)
    messages =dbConnect.getMessageAll(cid)
    
    return render_template('detail.html', messages=messages ,channle=channle)

if __name__ == '__main__':
    app.run(debug=True)

