import json
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper

from config import db


def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


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
