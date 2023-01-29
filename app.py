
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


    
    
    
    
    
    
    
    
    
    
    
    
    #62行目　？？？？？1/27このメッセージIDはHTMLから持ってきているとして、作成のところに書いてあるmessageはvalueじゃないからなんだ？ inputのnameからだ
    #cidはなんだ？どこから？  
    #HTMLのvalueは初期値を入れるところ　サーバーに送信する値のこと
