from flask import Flask, request, redirect, render_template, session, flash, url_for
from models import DbConnect
from util.user import User
from datetime import timedelta
from flask_paginate import Pagination, get_page_parameter
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
    db_user = DbConnect.getRegisteredUser(user_name, email)

    if db_user != None:
        flash('既に登録されているようです')
        return redirect('/signup')

    # 同一のユーザーが存在しなければ、登録する
    user_id = uuid.uuid4()
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    user = User(user_id, user_name, email, password)
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
        return redirect('/login')

    user = DbConnect.getUserByEmail(email)
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

    channels = DbConnect.getChannelAll(user_id)

    # ページネーション処理
    page = request.args.get(get_page_parameter(), type=int, default=1)
    rows = channels[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(channels), per_page=10)

    return render_template('index.html', channels=rows, pagination=pagination, user_id=user_id)


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

    if channel_name == "":
        flash('チャンネル名を入力してください')
        return redirect('/create-channel')

    channel = DbConnect.getChannelByName(channel_name)

    if channel != None:
        flash('既に同じチャンネルが存在しています。チャンネル名を変更してください。')
        return redirect('/create-channel')

    channel_description = request.form.get('channel-description')
    DbConnect.addChannel(user_id, channel_name, channel_description)

    # 作成したチャンネルのchannel_idを取得し、user_idと紐付け
    channel = DbConnect.getChannelByName(channel_name)
    DbConnect.addChannelUser(user_id, channel["channel_id"])
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


# チャンネル削除確認画面の表示
@app.route('/delete-channel/<channel_id>')
def delete_channel_page(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel = DbConnect.getChannelById(channel_id)
    return render_template('delete-channel.html', channel=channel)


# チャンネル削除機能
@app.route('/delete/<channel_id>')
def delete_channel(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel = DbConnect.getChannelById(channel_id)
    if user_id != channel['user_id']:
        flash('チャンネルは作成者のみ削除可能です')
        return redirect('/')

    DbConnect.deleteChannel(channel_id)

    return redirect('/')


# メッセージ一覧機能
@app.route('/detail/<channel_id>')
def detail(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = channel_id

    channel_user = DbConnect.getChannelUser(user_id, channel_id)
    if channel_user is None:
        flash('招待されていないチャンネルには参加できません')
        return redirect('/')

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
    return render_template('detail.html', messages=messages ,channel=channel, user_id=user_id)


# マイページ表示
@app.route('/mypage')
def getUserDetail():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    userDetail = DbConnect.getUserDetail(user_id)
    return render_template('user_detail.html', userDetail=userDetail, user_id=user_id)


# ユーザー招待画面の表示
@app.route('/user_invitation/<channel_id>')
def userInvitation(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel = DbConnect.getChannelById(channel_id)

    return render_template('user-invitation.html', channel=channel)


# ユーザー招待機能
@app.route('/user_invitation', methods=['POST'])
def addUser():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    channel_id = request.form.get('channel_id')
    user_name = request.form.get('user_name')

    if user_name == "":
        flash('ユーザー名を入力してください')
        return redirect(url_for('userInvitation', channel_id=channel_id))

    user =  DbConnect.getUserByName(user_name)

    if user is None:
        flash('ユーザー名が間違っています')
        return redirect(url_for('userInvitation', channel_id=channel_id))

    inv_user_id = user['user_id']

    channel_user = DbConnect.getChannelUser(inv_user_id, channel_id)

    if channel_user :
        flash('既に招待済みです')
        return redirect(url_for('userInvitation', channel_id=channel_id))

    DbConnect.addChannelUser(inv_user_id, channel_id)

    channel = DbConnect.getChannelById(channel_id)
    messages = DbConnect.getMessageAll(channel_id)
    return render_template('detail.html', messages=messages, channel=channel, user_id=user_id)


# チャンネルユーザー一覧機能
@app.route('/channel_users/<channel_id>')
def userList(channel_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    users = DbConnect.getChannelUserAll(channel_id)

    return render_template('channel-users.html', users=users, channel_id=channel_id)

if __name__ == '__main__':
    app.run(debug=True)