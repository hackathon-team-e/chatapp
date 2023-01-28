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


if __name__ == '__main__':
    app.run(debug=True)