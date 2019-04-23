from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity  # our own security.py
from resources.user_resource import UserRegister
from resources.item_resource import Item, ItemList
from resources.store_resource import Store, StoreList

app = Flask(__name__)

# tell the app where the db is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# turn off Flask's SQLALCHEMY modifications tracker (not the underlying one)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'smalls'
api = Api(app)


# Before any requests are made, create data.db and all required tables, unless
# they already exist.
@app.before_first_request  # this is a Flask decorator
def create_tables():
    db.create_all()
    # can only create the tables it 'sees'. It's important to import
    # everything we need SQLAlchemy to see, and create tables for.


jwt = JWT(app, authenticate, identity)

# ENDPOINTS / RESOURCES
api.add_resource(UserRegister, '/register')
# http://127.0.0.1:5000/register

api.add_resource(Item, '/item/<string:name>')
# e.g. http://127.0.0.1:5000/item/thing

api.add_resource(ItemList, '/items')
# i.e. http://127.0.0.1:5000/items

api.add_resource(Store, '/store/<string:name>')

api.add_resource(StoreList, '/stores')

# this makes sure that this line is executed only if this file - app.py
# was explicitly run by Python, i.e. not imported by another file.
# importing a module in Python runs executable lines
# when you run a python file, python assigns it __main__
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    '''
    why are we importing here?
    short answer: circular imports.
    '''

    app.run(port=5000, debug=True)
