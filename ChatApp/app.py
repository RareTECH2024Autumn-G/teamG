from flask import Flask,render_template,request,flash,redirect,session
from datetime import timedelta
import uuid
import hashlib
import re
import sys
import os

# 現在のディレクトリをPythonのパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import dbConnect
import pymysql

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# 接続した時のログインページを表示
@app.route('/')
def index():
    return redirect('/login')

# 接続した時のサインアップページを表示
@app.route('/signup')
def signup():
    return render_template('pages/register-pages/signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    sex = request.form.get('sex')
    mailaddress = request.form.get('mailaddress')
    password = request.form.get('password')
    passwordConfirm = request.form.get('passwordConfirm')
    sharehouse_id = request.form.get('sharehouseid')
    firstlogin = 1 #2024118 うっちゃん firstloginを追加    

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if name == '' or mailaddress =='' or password == '' or passwordConfirm == '' or sex == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirm:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, mailaddress) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(mailaddress)

        if DBuser != None:
            flash('すでに登録されています')
        else:
            #2024118 うっちゃん firstloginを追加    
            dbConnect.createUser(uid, name, mailaddress, password,sex,sharehouse_id,firstlogin)
            #2024118 End うっちゃん firstloginを追加    
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/login')
    return redirect('/signup')

# ログインページの表示
@app.route('/login', methods = ['GET'])
def displayLogin():
    return render_template('pages/register-pages/login.html')

#ログイン機能
@app.route('/login', methods=['POST'])
def userLogin():
    mailaddress = request.form.get('mailaddress')
    password = request.form.get('password')
    firstlogin = dbConnect.checkfirst(mailaddress)

    if mailaddress == '' or password == '':
        flash('メールアドレスおよびパスワードを入力してください')
        return redirect('/login') #2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
    else:
        user = dbConnect.getUser(mailaddress)

        if user is None:
            flash('このユーザーは存在しません')
            return redirect('/login')#2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword !=user['password']:
                flash('パスワードが違います')
                return redirect('/login')#2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
            else:
                # 2024/11/18 これが1回目のログインかを判別する（1の時は1回目のログイン、1以外の時は2回目以上のログイン）
                firstlogin = dbConnect.checkfirst(mailaddress)

                # 1回目のログインの時、初回グループ選択に遷移する
                if firstlogin['firstlogin'] == 1:
                    return redirect('/firstgroup')
                else: 
                    session['uid'] = user['uid']
                    return redirect('/home')        
    
# homeページの表示
@app.route('/home',methods = ['GET'])
def home():
    return render_template('pages/home-pages/home.html')

# first-groupページの表示(初回グループ選択画面)
@app.route('/firstgroup',methods = ['GET'])
def firstgroup():
    return render_template('pages/large-window-pages/first-group.html')

# first-groupで選択したものをusergroupsに格納する
@app.route('/select_firstgroup',methods = ['POST'])
def select_firstgroup():
    # 画面上でチェックされたチェックボックスを画面から受け取る
    services = request.form.getlist('group_id')  # 画面で複数選択されたサービスを受け取る
    print(f"app.py 118 DEBUG:選択されたサービスは{services}です")
    
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
        print(f"app.py 123 DEBUG：ログイン中のユーザーIDは→ {user_id}です")
    else:
        return "ログインしていません。"

    # もしserviceが選択されていたらusergruopsに登録処理
    if services != None:
        dbConnect.registsevices(user_id,services)

    # ユーザーが存在するか確認
    user = dbConnect.checkfirstuser(user_id) 
    if user != None:
        # 初回ログインフラグを更新1→0へ
        dbConnect.updatefirstlogin(user_id)

    # ホーム画面を表示する
    return redirect('/home')

# second-groupページの表示
@app.route('/second-group')
def second_group():
    return render_template('pages/large-window-pages/second-group.html')


# MANA追記
# add-personalページの表示(友達追加画面)
@app.route('/addpersonal')
def addpersonal():
    return render_template('pages/large-window-pages/add-personal.html')

# add-groupページの表示(友達追加画面・グループ作成モード)
@app.route('/addgroup')
def addgroup():
    return render_template('pages/large-window-pages/add-group.html')

# make-groupページの表示(グループ作成画面)
@app.route('/makegroup')
def makegroup():
    return render_template('pages/large-window-pages/make-group.html')
# MANA追記

# 2024/11/20 yoneyama add start

#チャットメッセージ表示
#  グループ一覧からグループを選択したら
#  グループのチャットメッセージを表示する
@app.route('/message', methods=['GET'])
def showChatMessage():

    #セッションからuidを取得して変数uidに格納
    uid = session.get("uid")

    #変数uidがない（None）場合
    if uid is None:

        #login.html（ログイン画面）に戻る
        return redirect('/login')

    #画面から受け取った選択中のグループ名（groupname）から
    l_groupname = request.form.get('groupname')

    #グループ情報をDB取得＝＞DB：getGroup
    #取得した結果をgroup変数に格納
    l_group = dbConnect.getGroup(l_groupname)

    #画面から受け取った選択中のグループID（groupid）から
    #選択中グループのメッセージをDB取得＝＞DB：getMessage
    #取得した結果をgroupmessage変数に格納
    l_groupmessage = dbConnect.getMessage(groupid)

    #home.html（ホーム画面（グループ））を呼び出す（引数：group、getMessage、uid）
    return render_template('home.html', group=l_group , groupmessage=l_groupmessage, uid=uid)

# 2024/11/20 yoneyama add end

    # ダミーデータで定義↓↓↓↓（画面の確認できないため）削除しても問題ない　アナザー　2024/11/21

@app.route('/chat/<cid>')
def chat(cid):
    channel = {
        "id": cid,
        "name": f"{cid}",
        "abstract": "このチャットルームについての説明!!!!!!!!!!!!!!!!!!!!!!!!。"
    }
    messages = [
        {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "こんにちは！", "created_at": "11/17 10:00"},
        {"id": 2, "user_id": 102, "user_name": "MANA", "content": "元気ですか？", "created_at": "11/17 10:05"},
        {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
        {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
        {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
       {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
       {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
       {"id": 1, "user_id": 101, "user_name": "アナザー", "content": "元気！", "created_at": "11/17 10:20"},
    ]
    return render_template('pages/home-pages/chat.html', channel=channel, messages=messages)
 # ダミーデータで定義↑↑↑↑（画面の確認できないため）
    # テンプレートに渡す　削除しても問題ない　アナザー　2024/11/21


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False)
# 2024/11/19 うっちゃん：デバッグのために仕込みdebug=Trueの時、上のprintたちがターミナルに出力される。
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )