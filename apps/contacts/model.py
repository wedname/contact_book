from datetime import datetime

from config import db


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # img = db.Column(db.String(250), default='some_path')
    name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(90), unique=True, nullable=False)
    email = db.Column(db.String(130))
    group = db.Column(db.String(130))
    address = db.Column(db.String(255))
    birthday = db.Column(db.String(90))
    note = db.Column(db.String(2000))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Contacts {self.id}>'

