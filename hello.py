from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your brower is %s</h1>' % user_agent

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>'%name

if __name__ == "__main__":
    manager.run()