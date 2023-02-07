from flask import Flask, request, redirect, render_template, session, flash
from models import dbConnect
from util.user import User
from datetime import timedelta
import hashlib
import uuid
import re


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# ユーザー登録画面の表示
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')


# ユーザー登録処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email =='' or password1 == '' or password2 == '':
        flash('空のフォームがあるようです')
    elif password1 != password2:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        user = User(uid, name, email, password)
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されているようです')
        else:
            dbConnect.createUser(user)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')


# ログイン画面の表示
@app.route('/login')
def login():
    return render_template('login.html')


# ログイン機能 
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')


# ログアウト機能
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# チャンネル一覧画面の表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    channels = dbConnect.getChannelAll()
    return render_template('index.html', channels=channels, uid=uid)


# チャンネル作成機能
@app.route('/', methods=['POST'])
def add_channel():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

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
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    return render_template('update-channel.html', channel=channel)


# チャンネル編集機能
@app.route('/update_channel/<cid>', methods=['POST'])
def update_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    cid = cid
    channel_name = request.form.get('channel-title')
    channel_description = request.form.get('channel-description')

    dbConnect.updateChannel(channel_name, channel_description, cid)
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)
    return render_template('detail.html', messages=messages, channel=channel, uid=uid)


# チャンネル削除機能
@app.route('/delete/<cid>')
def delete_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    dbConnect.deleteChannel(cid)
    channels = dbConnect.getChannelAll()
    return render_template('index.html', channels=channels)


# メッセージ一覧機能
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid) 
    return render_template('detail.html', messages=messages, channel=channel,uid=uid)


# メッセージの作成機能
@app.route('/message', methods=['POST'])
def add_message():
    uid = session.get('uid')
    if uid is None:
        return redirect('/login')

    message = request.form.get('message')
    channel_id = request.form.get('channel_id')
    if message:
        dbConnect.createMessage(channel_id, message)
    channel = dbConnect.getChannelById(channel_id)
    messages = dbConnect.getMessageAll(channel_id)
    return render_template('detail.html',messages=messages, channel=channel, uid=uid)


# メッセージの削除機能
@app.route('/delete_message', methods=['POST'])
def delete_message():

    message_id = request.form.get('message_id')
    cid = request.form.get('channel_id')

    if message_id:
        dbConnect.deleteMessage(message_id)
    channel =dbConnect.getChannelById(cid)
    messages =dbConnect.getMessageAll(cid)
    return render_template('detail.html', messages=messages ,channel=channel)


# おまじない
if __name__ == '__main__':
    app.run(debug=True)