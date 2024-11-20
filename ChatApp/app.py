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

# 11/15/04:20 localでのフロントなしAPIテスト
from flasgger import Swagger
# end 11/15/04:20 localでのフロントなしAPIテスト

# 11/15/04:30 DB接続
from flask_sqlalchemy import SQLAlchemy
import pymysql
# end 11/15/04:30 DB接続

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# 11/15/04:20 localでのフロントなしAPIテスト
# swagger = Swagger(app)
# end 11/15/04:20 localでのフロントなしAPIテスト

# 11/15/04:30 DB接続
# SQLAlchemy 設定 (MySQL接続)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testuser:testuser@db:3306/sharehappy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# end 11/15/04:30 DB接続

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
    sharehouseid = request.form.get('sharehouseid')
    #2024118 うっちゃん firstloginを追加    
    firstlogin = 1

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
            dbConnect.createUser(uid, name, mailaddress, password,sex,sharehouseid,firstlogin)
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
    # print(f"app.py 101 DEBUG: checkfirst(mailaddress) = {firstlogin}")  # 戻り値を出力【削除すること！！！】

    if mailaddress == '' or password == '':
        flash('メールアドレスおよびパスワードを入力してください')
        return redirect('/signup') #2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
    else:
        user = dbConnect.getUser(mailaddress)

        if user is None:
            flash('このユーザーは存在しません')
            return redirect('/signup')#2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword !=user['password']:
                flash('パスワードが違います')
                return redirect('/signup')#2024/11/19 うっちゃん エラー時ログイン画面に止まるように変更
            else:
                # 2024/11/18 これが1回目のログインかを判別する（1の時は1回目のログイン、1以外の時は2回目以上のログイン）
                firstlogin = dbConnect.checkfirst(mailaddress)
                # print(f"app.py 121 DEBUG: firstlogin = {firstlogin}")  # 戻り値を出力【削除すること！！！】                

                # 1回目のログインの時、初回グループ選択に遷移する
                if firstlogin['firstlogin'] == 1:
                    return redirect('/firstgroup')
                else: 
                    session['uid'] = user['uid']
                    return redirect('/home')        
    
# homeページの表示
@app.route('/home')
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
    try:
        # リクエストからJSONデータを取得
        data = request.get_json()
        group_id = data.get('group_id')
        print(f"app.py 142 DEBUG: group_id = {group_id}")  # 戻り値を出力【削除すること！！！】

        if not group_id:
            return jsonify({"error": "グループIDが指定されていません"}), 400

        # グループIDの処理 (例: データベースに保存)
        # ここでユーザー情報と選択されたグループを保存する処理を追加できます。
        # 例: user.selected_group_id = group_id

        return jsonify({"message": f"グループ {group_id} が選択されました！"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # 画面上でチェックされたチェックボックスの内容でusergruopsに登録を行う
    # 初回ログインフラグを更新1→0へ
    # ホーム画面を表示する
    return render_template('pages/large-window-pages/first-group.html')

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


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=False)
# 2024/11/19 うっちゃん：デバッグのために仕込みdebug=Trueの時、上のprintたちがターミナルに出力される。
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )