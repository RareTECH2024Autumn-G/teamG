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
            dbConnect.createUser(uid, name, mailaddress, password,sex,sharehouseid)
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

    if mailaddress == '' or password == '':
        flash('メールアドレスおよびパスワードを入力してください')
    else:
        user = dbConnect.getUser(mailaddress)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword !=user['password']:
                flash('パスワードが違います')
            else:
                session['uid'] = user['uid']
                return redirect('/home')
        return redirect('/signup')
    
# homeページの表示
@app.route('/home')
def home():
    return render_template('pages/home-pages/home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
