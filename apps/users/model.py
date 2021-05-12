from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,  check_password_hash

from config import db, login_manager
from apps.contacts.model import Contacts


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # img = db.Column(db.String(250), default='some_path')
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    phone = db.Column(db.String(90), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    contacts = db.relationship('Contacts', backref='users', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.id}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


db.create_all()
