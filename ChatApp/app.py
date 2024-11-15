from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

# 11/15/04:20 localでのフロントなしAPIテスト
from flasgger import Swagger
# end 11/15/04:20 localでのフロントなしAPIテスト

# 11/15/04:30 DB接続
from flask_sqlalchemy import SQLAlchemy
import pymysql
# end 11/15/04:30 DB接続

app = Flask(__name__)

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

# ログインページの表示
@app.route('/login',methods = ['GET'])
def display_login():
    return render_template('pages/register-pages/login.html')


#ログイン機能
@app.route('/login',methods = ['POST'])
def login():
    email = request.form.get('username') #20241115_20:40_まなさんのに合わせました
    password = request.form.get('password') #20241115_20:40_まなさんのに合わせました
    return render_template('pages/register-pages/signup.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
