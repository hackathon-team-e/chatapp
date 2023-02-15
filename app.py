from flask import Flask, request, redirect, render_template, session, flash
from models import DbConnect
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
    return render_template('signup.html')


# ユーザー登録処理
@app.route('/signup', methods=['POST'])
def userSignup():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "[\w\-._]+@[\w\-._]+\.[A-Za-z]+"

    if user_name == '' or email =='' or password1 == '' or password2 == '':
        flash('空のフォームがあります')
        return redirect('/signup')

    if password1 != password2:
        flash('パスワードが一致していません')
        return redirect('/signup')

    if re.fullmatch(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
        return redirect('/signup')

    # 同一のユーザー名、emailのユーザーが登録されているか確認
    dbUser = DbConnect.getRegisteredUser(user_name, email)

    if dbUser != None:
        flash('既に登録されているようです')
        return redirect('/signup')

    user_id = uuid.uuid4()
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    user = User(user_id, user_name, email, password)


    # 同一のユーザーが存在しなければ、登録する
    DbConnect.createUser(user)
    user_id = str(user_id)
    session['user_id'] = user_id
    return redirect('/')


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
        flash('空のフォームがあります')
        return redirect('/')

    user = DbConnect.getUser(email)
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if user is None or hashPassword != user["password"]:
        flash('EmailまたはPasswordが間違っています')
        return redirect('/login')
    
    session['user_id'] = user["user_id"]
    return redirect('/')


# ログアウト機能
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# チャンネル一覧画面の表示
@app.route('/')
def index():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')

    channels = DbConnect.getChannelAll()
    return render_template('index.html', channels=channels, user_id=user_id)


# チャンネル作成画面の表示
@app.route('/create-channel')
def create_channel():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    
    return render_template('create-channel.html')

# チャンネル作成機能
@app.route('/create-channel', methods=['POST'])
def add_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_name = request.form.get('channel-title')
    channel = DbConnect.getChannelByName(channel_name)

    if channel != None:
        error = '既に同じチャンネルが存在しています。チャンネル名を変更してください。'
        return render_template('error/error.html', error_message=error)

    channel_description = request.form.get('channel-description')
    DbConnect.addChannel(user_id, channel_name, channel_description)
    return redirect('/')


# チャンネル編集画面の表示
@app.route('/update_channel/<channel_id>')
def update_channel_page(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = channel_id
    channel = DbConnect.getChannelById(channel_id)
    return render_template('update-channel.html', channel=channel)


# チャンネル編集機能
@app.route('/update_channel/<channel_id>', methods=['POST'])
def update_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = channel_id
    channel_name = request.form.get('channel-title')
    channel_description = request.form.get('channel-description')

    DbConnect.updateChannel(user_id, channel_name, channel_description, channel_id)
    channel = DbConnect.getChannelById(channel_id)
    messages = DbConnect.getMessageAll(channel_id)
    return render_template('detail.html', messages=messages, channel=channel, user_id=user_id)


# チャンネル削除確認画面にの表示
@app.route('/delete-channel/<channel_id>')
def delete_channel_page(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = channel_id
    channel = DbConnect.getChannelById(channel_id)
    return render_template('delete-channel.html', channel=channel)


# チャンネル削除機能
@app.route('/delete/<channel_id>')
def delete_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    DbConnect.deleteChannel(channel_id)
    channels = DbConnect.getChannelAll()
    return render_template('index.html', channels=channels)


# メッセージ一覧機能
@app.route('/detail/<channel_id>')
def detail(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = channel_id
    channel = DbConnect.getChannelById(channel_id)
    messages = DbConnect.getMessageAll(channel_id) 
    return render_template('detail.html', messages=messages, channel=channel, user_id=user_id)


# メッセージの作成機能
@app.route('/message', methods=['POST'])
def add_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    message = request.form.get('message')
    channel_id = request.form.get('channel_id')
    if message:
        DbConnect.createMessage(user_id, channel_id, message)
    channel = DbConnect.getChannelById(channel_id)
    messages = DbConnect.getMessageAll(channel_id)
    return render_template('detail.html', messages=messages, channel=channel, user_id=user_id)


# メッセージの削除機能
@app.route('/delete_message', methods=['POST'])
def delete_message():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    message_id = request.form.get('message_id')
    channel_id = request.form.get('channel_id')

    if message_id:
        DbConnect.deleteMessage(message_id)
    channel = DbConnect.getChannelById(channel_id)
    messages = DbConnect.getMessageAll(channel_id)
    return render_template('detail.html', messages=messages ,channel=channel)


if __name__ == '__main__':
    app.run(debug=True)