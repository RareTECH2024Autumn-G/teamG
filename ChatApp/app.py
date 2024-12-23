from flask import Flask,render_template,request,flash,redirect,session
from datetime import timedelta
import uuid
import hashlib
import re
import sys
import os
import datetime # 2024/11/21 yoneyama add

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

    if name == '' or mailaddress =='' or password == '' or passwordConfirm == '' or sex is None: #2024118 タラ　sex is None　に変更
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
            # 2024/11/18 うっちゃん firstloginを追加    
            dbConnect.createUser(uid, name, mailaddress, password,sex,sharehouse_id,firstlogin)
            
            # # 2024/11/22 うっちゃん 初回グループ登録
            # print(f"app.py 60 デバッグ:通っているぞ{sex}")

            if sex == 'man':
                sexcid = 2
            elif sex == 'woman':
                sexcid = 3
            dbConnect.registrequiregroups(uid,sexcid)

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
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    groups = dbConnect.getbelonggroups(user_id) #user_idをもとにデータベースのusergroupsのデータを取得
    if groups != None: #resultsが空欄でない場合画面にデータを引き渡す
        # print(f"app.py 122 デバッグ:通っているぞ{groups}")
        return render_template('pages/home-pages/home.html', groups=groups)
    else:
        return "グループが存在しません。"

# first-groupページの表示(初回グループ選択画面)
@app.route('/firstgroup',methods = ['GET'])
def firstgroup():
    return render_template('pages/large-window-pages/first-group.html')

# first-groupで選択したものをusergroupsに格納する
@app.route('/select_firstgroup',methods = ['POST'])
def select_firstgroup():
    # 画面上でチェックされたチェックボックスを画面から受け取る
    selectgroups = request.form.getlist('group_id')  # 画面で複数選択されたサービスを受け取る
    # print(f"app.py 118 DEBUG:選択されたサービスは{selectgroups}です")

    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"

    # もしselectgroupsが選択されていたらusergruopsに登録処理
    if selectgroups != None:
        dbConnect.registgroups(user_id,selectgroups)
        # print(f"app.py 147 デバッグ:通っているぞ{selectgroups}")

    # ユーザーが存在するか確認
    user = dbConnect.checkfirstuser(user_id) 
    # print(f"app.py 151 デバッグ:通っているぞ")
    if user != None:
        # 初回ログインフラグを更新1→0へ
        dbConnect.updatefirstlogin(user_id)
        # print(f"app.py 155 デバッグ:通っているぞ")

    # ホーム画面を表示する
    return redirect('/home')

# secondgroupページの表示（2024/11/22 既存グループ選択画面 うっちゃん）
@app.route('/secondgroup',methods = ['GET'])
def secondgroup():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    allgroups = dbConnect.getallgroups(user_id) 
    # print(f"app.py 171 デバッグ:通っているぞ{allgroups}")

    if not allgroups:
        flash('未加入のグループが存在しません。')
        return redirect('/home')
    else:
        return render_template('pages/large-window-pages/second-group.html', allgroups=allgroups)

# 既存グループ追加（2024/11/25 既存グループ登録 うっちゃん）
@app.route('/joingroup',methods = ['POST'])
def joingroup():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    # 画面から取得したグループ名でINSERTする
    selectgroups = request.form.get('allgroup_id')
    print(f"app.py 191 DEBUG:選択されたグループは{selectgroups}です")
    dbConnect.registgroups(user_id,selectgroups)

    # チャット画面に遷移する
    return redirect('/home')
    
# MANA追記
# add-personalページの表示(友達追加画面)
# 2024/11/23　タラ追記(addpersonalにユーザー一覧データ渡す)
@app.route('/addpersonal',methods = ['GET'])
def addpersonal():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        uid = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    users = dbConnect.getallusers(uid) #user_idをもとにデータベースのusergroupsのデータを取得
    print(f"app.py 209 DEBUG:選択されたユーザーは{users}です")
    return render_template('pages/large-window-pages/add-personal.html',users = users)

# 2024/11/28 うっちゃん 個人チャットを開始
@app.route('/addpersonal',methods = ['POST'])
def joinpersonalchat():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        uid = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    # 選択した人とのGを追加する
    selectUsers = request.form.getlist('selectUserid')
    selectUsername = request.form.getlist('selectUsername')
    print(f"app.py 222 DEBUG:選択されたユーザーは{selectUsers}:{selectUsername}です")
    required = '1'
    comment = ''
    cid = dbConnect.createGroup(selectUsername,required,comment)
    dbConnect.addGroup(selectUsers,cid)
    print(f"app.py 229 DEBUG:選択されたユーザーは{uid}です")
    uid_list = [uid]
    dbConnect.addGroup(uid_list,cid)
    return redirect("/home")

# 2024/11/23　タラ追記(addpersonalで選択したユーザーデータをmake-groupに渡す)
@app.route('/select-addpersonal',methods = ['POST'])
def select_addpersonal():
        # 画面上でチェックされたチェックボックスを画面から受け取る
    selectUsers = request.form.get('selectUser')  # 画面で複数選択されたサービスを受け取る
    print(f"app.py 198 DEBUG:選択されたユーザーは{selectUsers}です")

    if selectUsers is None:
        flash('追加するメンバーを選択してください')
    else:
    # セッションに保存
        session['selectUsers'] = selectUsers
        return render_template('pages/large-window-pages/make-group.html', selectUsers = selectUsers)
    return redirect("/addgroup")


# add-groupページの表示(友達追加画面・グループ作成モード)
# 2024/11/23　タラ追記(addgroupにユーザー一覧データ渡す)
@app.route('/addgroup',methods = ['GET'])
def addgroup():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        uid = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"   
    users = dbConnect.getallusers(uid) #user_idをもとにデータベースのusergroupsのデータを取得
    return render_template('pages/large-window-pages/add-group.html', users = users)

# make-groupページの表示(グループ作成画面)
@app.route('/makegroup',methods = ['GET'])
def makegroup():
    return render_template('pages/large-window-pages/make-group.html')
# MANA追記

# 2024/11/23　タラ追記(addgroupから受け取ったselectUsersの情報と合わせて、home画面に戻る)
@app.route('/makegroup',methods = ['POST'])
def make_newGroup():
    name = request.form.get("name")
    required = request.form.get("required")
    comment = request.form.get("comment")

    # セッションから'uid',`selectUsers`を取得
    uid = session.get("uid")
    selectUser = session.get('selectUsers')
    selectUsers = [uid,*selectUser]
    print(f"app.py 242 DEBUG:selectUsers = {selectUsers}です")

    if name == "":
        flash("グループ名を入力してください！")
    else:
        cid = dbConnect.createGroup(name,required,comment)
        dbConnect.addGroup(selectUsers,cid)
        return redirect("/home")
    return redirect("/makegroup")

# チャット内容を表示する 2024/11/28
@app.route('/chat/<cid>')
def chat(cid):
    channel = dbConnect.getGroup(cid)

    messages = dbConnect.getMessage(cid)
    print(f"app.py 327 DEBUG: messages={messages}")
    return render_template('pages/home-pages/chat.html', channel=channel, messages=messages)

# 2024/11/23 yoneyama add start
#チャットメッセージ送信
#  グループに向けたチャットを送信する

# @app.route('/chat', methods=['POST'])
# def sendChatMessage():

#     #セッションからuidを取得して変数uidに格納
#     uid = session.get("uid")

#     #変数uidがない（None）場合
#     if uid is None:

#         #login.html（ログイン画面）に戻る
#         return redirect('/login')

#     #画面からメッセージを受け取り、変数messageに格納する
#     l_message = request.form.get('message')
#     print(f"app.py 348 DEBUG: l_message={l_message}")

#     #画面からグループIDを受け取り、変数group_idに格納
#     #l_group_id = request.form.get(”group_id”) #dockers compose upしたらエラー
#     l_group_id = request.form.get('cid')
#     print(f"app.py 353 DEBUG: l_group_id={l_group_id}")

#     #日付を取得＝＞DateTime
#     l_datetime = datetime.datetime.now()
#     print(f"app.py 357 DEBUG: l_datetime={l_datetime}")

#     #変数messageが存在する場合
#     if l_message:

#         #メッセージ内容をDBに登録＝＞DB：createMessageのコール
#         dbConnect.createMessage(uid ,l_group_id ,l_datetime ,l_message)

#     #chat.html（チャット画面）を再表示?
#     return render_template('chat.html')

@app.route('/message', methods=['POST'])
def sendChatMessage():
    print(f"messages2:")
    #セッションからuidを取得して変数uidに格納
    uid = session.get("uid")
    print(f"uid:{uid}")

    #変数uidがない（None）場合
    if uid is None:
        #login.html（ログイン画面）に戻る
        return redirect('/login')

    #画面からメッセージを受け取り、変数messageに格納する
    l_message = request.form.get('message')
    print(f"messages3:{l_message}")

    #画面からグループIDを受け取り、変数group_idに格納
    #l_group_id = request.form.get(”group_id”) #dockers compose upしたらエラー
    l_group_id = request.form.get('cid')
    print(f"l_group_id: {l_group_id}")

    #日付を取得＝＞DateTime
    l_datetime = datetime.datetime.now()
    print(f"l_datetime: {l_datetime}")

    #変数messageが存在する場合
    if l_message:

        #print(f"messages3:")
        #メッセージ内容をDBに登録＝＞DB：createMessageのコール
#        print(f"l_group_id:" + l_group_id)
#        print(f"l_message:" + l_message)
        dbConnect.createMessage(uid ,l_group_id ,l_datetime ,l_message)

    #chat.html（チャット画面）を再表示?
#    return render_template('chat.html')
#    return redirect('/login')
    # return redirect('/chat/{cid}'.format(cid = l_group_id))
    return redirect(request.referrer)

# 2024/11/23 yoneyama add end

#MANA追記2→2024/11/25 うっちゃん更新
#setting-accountページの表示（アカウント管理画面）
@app.route('/setting-page',methods = ['GET'])
def setting_page():
    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"
    
    # DBから現在の情報を取得する
    userinfo = dbConnect.getuserinfo(user_id)
    if userinfo != None: #resultsが空欄でない場合画面にデータを引き渡す
        print(f"app.py 378 デバッグ:通っているぞ{userinfo}")
        return render_template('pages/setting-account.html', userinfo=userinfo)
    else:
        return "データの取得に失敗しました。"
# MANA追記

# アカウント情報更新 2024/11/25 うっちゃん更新
@app.route('/setting-page',methods = ['POST'])
def updateuserinfo():
    name = request.form.get('newName', '')
    comment = request.form.get('newcomment', '')
    mailaddress = request.form.get('newMailAddress', '')
    password = request.form.get('settingNewPassword', '')
    passwordConfirm = request.form.get('SNPConfirm', '')
    sharehouse_id = request.form.get('settingSharehouseId', '')

    # セッションにユーザーIDが保存されているか確認
    if 'uid' in session:  
        user_id = session['uid']  # 現在のユーザーのIDを取得
    else:
        return "ログインしていません。"

    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if name == '' or password == '' or mailaddress == ''  or passwordConfirm == '' or sharehouse_id == '': 
        flash('空のフォームがあるようです')
    elif password != passwordConfirm:
        flash('二つのパスワードの値が違っています')
    elif re.match(pattern, mailaddress) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        # uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(mailaddress)

        if DBuser == None:
            flash('ユーザー情報が存在しません')
            return redirect('/setting-page')
        else:
            dbConnect.updateuserinfo(user_id, name, mailaddress, password,sharehouse_id,comment)
            return redirect('/home')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False)
# 2024/11/19 うっちゃん：デバッグのために仕込みdebug=Trueの時、上のprintたちがターミナルに出力される。
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000
    )