from db import db

# user model - our internal representation of an entity
# whereas a Resource is the external representation of an entity
# A model should contain info & functionality not directly accessed
# through API.


# extends db.Model - i.e. SQLAlchemy's model
class ItemModel(db.Model):
    # tell SQLAlchemy what table this model involves
    __tablename__ = 'items'

    # tell SQLAlchemy what columns are in the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # create a column with foreign key reference to id of a store
    # note: if a store is referenced by a foreign key, it cannot be deleted
    # gives functionality, plus control and some security.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # this is SQLAlchemy handling SQL 'joins'

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):

        # return a dict representing our item.
        # necessary now that our find_by_name() method returns an ItemModel
        # object instead of json. We can't return an object to client.
        # See the get() method in Item(Resource) for an example use.

        return {'name': self.name, 'price': self.price}

    # this remains a class method as per v2, because it now returns an object
    # of type ItemModel as opposed to a dictionary
    @classmethod
    def find_by_name(cls, name):  # cls because class method
        return cls.query.filter_by(name=name).first()

        # excluding all the connections stuff, the above is equivalent to:
        # SELECT * FROM items WHERE name=name LIMIT 1
        #
        # NB: This returns an ItemModel object
        #
        # .query() comes from SQLAlchemy, available since ItemModel
        # extends db.Model
        # Much easier than before - handling the db connection, cursor and
        # creating SQL queries.

    def save_to_db(self):
        # with SQLAlchemy, insert & update can both be handled by add()
        # insert changed to save_to_db() - aka 'upsert'. update() removed
        db.session.add(self)
        db.session.commit()

    # changed this from v2 from class method to 'self' since it is
    # updating itself
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

