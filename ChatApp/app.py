from flask import Flask, render_template

app = Flask(__name__)

@app.route('/signup')
def signup():
    return render_template('pages/register-pages/signup.html')

@app.route('/login')
def login():
    return render_template('pages/register-pages/login.html')

if __name__ == '__main__':
    app.run()