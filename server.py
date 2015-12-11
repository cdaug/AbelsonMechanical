from flask import Flask, flash, render_template, request, session, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
# TODO: Implement SQLAlchemy

DEBUG=True

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"

db = SQLAlchemy(app)

engine = sqlalchemy.create_engine('sqlite:////abelson.db', echo=True)
Base = sqlalchemy.ext.declarative.declarative_base()
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

class Locations(Base):
    __tablename__ = "Locations"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    phone = Column(Integer)
    fax = Column(Integer)
    email = Column(Integer)

class Jobs(Base):
    __tablename__ = "Jobs"

    id = sqlalchemy.Column(Integer, primary_key=True)
    title = sqlalchemy.Column(String)
    locations = sqlalchemy.Column(String)
    descition = sqlalchemy.Column(String)



login_manager = LoginManager()
login_manager.init_app(app)

Flask.secret_key = "random"

class UserNotFoundError(Exception):
    pass


# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    '''Simple User class'''
    USERS = {
        'admin':'password',
        'garrett':'password'
    }

    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.get(id)

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
    user = User.get(request.form['username'])
    if (user and user.password == request.form['password']):
        login_user(user)
        return redirect(url_for('admin'))
    else:
        flash('Username or password incorrect')

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/admin")
def admin():
    if current_user.is_authenticated == True:
        return render_template('admin.html')
    else:
        return redirect(url_for('index'))

@app.route("/careers", methods=['GET'])
def careers():
    return render_template('careers.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
