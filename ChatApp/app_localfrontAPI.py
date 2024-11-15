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


# 11/15/04:20 localでのフロントなしAPIテスト
@app.route('/hello', methods=['GET'])
def hello_world():
    """
    A simple hello world endpoint
    ---
    responses:
      200:
        description: A hello world response
        examples:
          application/json: {"message": "Hello, World!"}
    """
    return {"message":"Hello, World!"}
# end 11/15/04:20 localでのフロントなしAPIテスト

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
    # 11/15/04:20 localでのフロントなしAPIテスト
    """
    ログインページを表示するエンドポイント
    ---
    responses:
      200:
        description: ログインページのHTMLを表示
        content:
          text/html:
            example: "<html>...</html>"
    """
    # end 11/15/04:20 localでのフロントなしAPIテスト
    return render_template('pages/register-pages/login.html')


#ログイン機能
@app.route('/login',methods = ['POST'])
def login():
    email = request.form.get('username') #20241115_20:40_まなさんのに合わせました
    password = request.form.get('password') #20241115_20:40_まなさんのに合わせました
    return render_template('pages/register-pages/signup.html')

# 20241115_うっちゃんDB接続テスト
# # 11/15/04:30 DB接続
# @app.route('/check_db', methods=['GET'])
# def check_db():
#     """
#     DB接続を確認するエンドポイント
#     ---
#     responses:
#       200:
#         description: DB接続が成功した場合
#         content:
#           application/json:
#             example: {"message": "DB接続成功"}
#       500:
#         description: DB接続に失敗した場合
#         content:
#           application/json:
#             example: {"message": "DB接続失敗"}
#     """
#     try:
#         # DB接続をチェック
#         result = db.session.execute('SELECT 1')
#         if result:
#             return {"message": "DB接続成功"}, 200
#     except Exception as e:
#         print(f"Error: {e}")  # エラーログに詳細を出力
#         return {"message": "DB接続失敗", "error": str(e)}, 500

# @app.route('/users', methods=['GET'])
# def get_users():
#     """
#     ユーザー情報を取得するエンドポイント
#     ---
#     responses:
#       200:
#         description: ユーザー情報のリスト
#         content:
#           application/json:
#             example: [
#                 {"id": 1, "name": "ユーザー名", "mailaddress": "user@example.com"}
#             ]
#       500:
#         description: データベースエラー
#     """
#     try:
#         users = db.session.execute('SELECT uid, user_name, email FROM users')
#         users_list = [dict(user) for user in users]
#         return {"users": users_list}, 200
#     except Exception as e:
#         return {"message": "DB接続失敗", "error": str(e)}, 500

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     """
#     新しいユーザーを追加するエンドポイント
#     ---
#     parameters:
#       - in: body
#         name: user
#         description: 新しいユーザーの情報
#         required: true
#         schema:
#           type: object
#           properties:
#             uid:
#               type: string
#             user_name:
#               type: string
#             email:
#               type: string
#             password:
#               type: string
#     responses:
#       200:
#         description: ユーザーの追加が成功した場合
#       500:
#         description: データベースエラー
#     """
#     data = request.get_json()
#     try:
#         new_user = f"""
#         INSERT INTO users (uid, user_name, email, password) 
#         VALUES ('{data['uid']}', '{data['user_name']}', '{data['email']}', '{data['password']}')
#         """
#         db.session.execute(new_user)
#         db.session.commit()
#         return {"message": "ユーザーの追加が成功しました"}, 200
#     except Exception as e:
#         db.session.rollback()
#         return {"message": "DB接続失敗", "error": str(e)}, 500



# # end 11/15/04:30 DB接続

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
