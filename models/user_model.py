from db import db


'''
user model - our internal representation of an entity
whereas a Resource is the external representation of an entity
A model should contain info & functionality not directly accessed
through API.
'''


# extends db.Model - i.e. SQLAlchemy's model
class UserModel(db.Model):
    # tell SQLAlchemy what table this model involves
    __tablename__ = 'users'

    # tell SQLAlchemy about the columns in this table
    id = db.Column(db.Integer, primary_key=True)
    # primary_key=True means this column is auto-incrementing
    # all handled by SQLAlchemy
    username = db.Column(db.String(80))  # character limit
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # note we don't specifiy an id as it will be automatically created
        # by SQLAlchemy, primary_key=True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # NB first 'username' is the column name, second is the passed in arg
        # since we know usernames are unique, we only need first() result
        # this returns an ItemModel object.

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # where id is the column and _id is the argument
