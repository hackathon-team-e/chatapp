
from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect
# from util.user import User
# from datetime import timedelta
# import hashlib
# import uuid
# import re

app = Flask(__name__)

# チャンネル一覧画面の表示
@app.route('/')
def index():
    channels = dbConnect.getChannelAll()
    return render_template('index.html', channels=channels)

@app.route("/create")
def create():
    return render_template('create.html')

# チャンネル作成機能
@app.route('/create', methods=['POST'])
def add_channel():
    channel_name = request.form.get('channel-title')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channel-description')
        dbConnect.addChannel(channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じチャンネルが存在しています。チャンネル名を変更してください。'
        return render_template('error/error.html', error_message=error)


# チャンネル編集画面の表示
@app.route('/update_channel/<cid>')
def update_channel_page(cid):
    cid = cid
    channel = dbConnect.getChannelById(cid)
    return render_template('update-channel.html', channel=channel)


# チャンネル編集機能
@app.route('/update_channel/<cid>', methods=['POST'])
def update_channel(cid):
    cid = cid
    channel_name = request.form.get('channel-title')
    channel_description = request.form.get('channel-description')
    dbConnect.updateChannel(channel_name, channel_description, cid)
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    return render_template('detail.html', messages=messages, channel=channel)


# チャンネル削除機能
@app.route('/delete/<cid>')
def delete_channel(cid):
    dbConnect.deleteChannel(cid)
    channels = dbConnect.getChannelAll()
    return render_template('index.html', channels=channels)


# メッセージ一覧機能
@app.route('/detail/<cid>')
def detail(cid):
    cid = cid
    channel =dbConnect.getChannelById(cid)
    messages =dbConnect.getMessageAll(cid) 
    return render_template('detail.html', messages=messages, channel=channel)


# メッセージの作成機能
@app.route('/message', methods=['POST'])
def add_message():
    message = request.form.get('message')
    channel_id = request.form.get('channel_id')
    if message:
        dbConnect.createMessage(channel_id, message)
    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)
    return render_template('detail.html',messages=messages, channel=channel)


# メッセージの削除機能
@app.route('/delete_message', methods=['POST'])
def delete_message():
    message_id = request.form.get('message_id')
    cid =request.form.get('channel_id')
    if message_id :
        dbConnect.deleteMessage(message_id)
    channle =dbConnect.getChannelById(cid)
    messages =dbConnect.getMessageAll(cid)
    return render_template('detail.html', messages=messages ,channle=channle)


# おまじない
if __name__ == '__main__':
    app.run(debug=True)