from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

DB_URI = 'sqlite:///contact_book.db'
APP_SECRET = 'asdasdasdasd'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = APP_SECRET

db = SQLAlchemy(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
