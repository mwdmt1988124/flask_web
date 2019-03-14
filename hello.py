from flask import Flask,flash
from flask import request
from flask import make_response,redirect,render_template,session,redirect,url_for
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message
import os

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:123456@localhost/flask_web?charset=utf8"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_PASSWORD'] = 'ymb1988124'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[民生保险]'
app.config['FLASKY_MAIL_SENDER'] ='Flasky Admin<136419201602@163.com>'
app.config['FLASKY_ADMIN'] = '344054296@qq.com'

db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)

def send_mail(to,subject,template,**kwargs):
    msg =Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                 sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+ '.html',**kwargs)
    mail.send(msg)

def make_shell_context():
    return dict(app = app,db = db , User = User , Role = Role)
manager.add_command("shell",Shell(make_context = make_shell_context))
manager.add_command('db' , MigrateCommand)

@app.route('/',methods = ['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',current_time =datetime.utcnow(),form = form,name=session.get('name'),
                           known = session.get('known',False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship("User",backref ='role',lazy = 'dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' %self.username

if __name__ == "__main__":
    manager.run()