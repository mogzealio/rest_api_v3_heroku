from db import db


'''
user model - our internal representation of an entity
whereas a Resource is the external representation of an entity
A model should contain info & functionality not directly accessed
through API.
'''


# extends db.Model - i.e. SQLAlchemy's model
class StoreModel(db.Model):
    # tell SQLAlchemy what table this model involves
    __tablename__ = 'stores'

    # tell SQLAlchemy what columns are in the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # tell SQLAlchemy that there is a relationship between StoreModel
    # and ItemModel, it will check what the relationship is.
    items = db.relationship('ItemModel', lazy='dynamic')
    # lazy='dynamic' tells SQLAlchemy NOT to look into the items table
    # and create an object for every item in the db, yet.
    # This requires .all() to be used when accessing items - see json() below.
    # This is all down to performance and where we want this work to happen.

    def __init__(self, name):
        self.name = name

    def json(self):
        # return a dict representing our item.
        # necessary now that our find_by_name() method returns an StoreModel
        # object instead of json. We can't return an object to client.

        return {'name': self.name,
                'items': [item.json() for item in self.items.all()]}
        # because of lazy='dynamic' relationship, we need to use all()
        # so that json() looks inside the items table.

    @classmethod
    def find_by_name(cls, name):  # cls because class method
        return cls.query.filter_by(name=name).first()

        # excluding all the connections stuff, the above is equivalent to:
        # SELECT * FROM items WHERE name=name LIMIT 1

        # NB: This returns an StoreModel object

        # .query() comes from SQLAlchemy, available since ItemModel
        # extends db.Model
        # Much easier than before - handling the db connection, cursor and
        # creating SQL queries.

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

