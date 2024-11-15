from flask import Flask, request, redirect, render_template, session, flash, abort
from datetime import timedelta
import hashlib
import uuid
import re

from models import dbConnect

from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# 接続した時のログインページを表示
@app.route('/')
def index():
    # uid = session.get("uid")
    # if uid is None:
    return redirect('/login')
    # else:
    #     channels = dbConnect.getChannelAll()
    #     channels.reverse()
    # return render_template('index.html', channels=channels, uid=uid)

# ログインページの表示
@app.route('/login',methods = ['GET'])
def display_login():
    return render_template('pages/register-pages/login.html')

#ログイン機能
@app.route('/login',methods = ['POST'])
def login():

    return render_template('pages/register-pages/login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
