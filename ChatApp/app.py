from flask import Flask, render_template, request,flash,redirect, session
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

# # 2024/11/18 VSCode上でデバックを行うためにインポート
# import pdb
# # End  2024/11/18 VSCode上でデバックを行うためにインポート

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

# 11/15/04:20 localでのフロントなしAPIテスト
swagger = Swagger(app)
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
    #2024118 End うっちゃん firstloginを追加    

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
@app.route('/login',methods = ['GET'])
def display_login():
    return render_template('pages/register-pages/login.html')

#ログイン機能
@app.route('/login', methods=['POST'])
def userLogin():
    mailaddress = request.form.get('mailaddress')
    password = request.form.get('password')
    #
    firstlogin = dbConnect.checkfirst('mailaddress')

    if mailaddress == '' or password == '':
        flash('メールアドレスおよびパスワードを入力してください')
    else:
        user = dbConnect.getUser(mailaddress)
        # pdb.set_trace()
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword !=user['password']:
                flash('パスワードが違います')
            else:
                # 2024/11/18 これが1回目のログインかを判別する
                # 0の時は1回目のログイン、1以外の時は2回目以上のログイン
                firstlogin = dbConnect.checkfirst('mailaddress')
                if firstlogin == 0:
                    return redirect('/first-group')
                else: 
                    session['uid'] = user['uid']
                    return redirect('/home')
                # End 2024/11/18 これが1回目のログインかを判別する
        return redirect('/signup')
    
# homeページの表示
@app.route('/home')
def home():
    return render_template('pages/home-pages/home.html')

# first-groupページの表示(初回グループ選択画面)
@app.route('/first-group')
def first_group():
    return render_template('pages/large-window-pages/first-group.html')


# second-groupページの表示
@app.route('/second-group')
def second_group():
    return render_template('pages/large-window-pages/second-group.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=False)
# 2024/11/19 うっちゃん：デバッグのために仕込んでみた。
if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )