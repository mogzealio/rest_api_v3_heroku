from app import app
from db import db

db.init_app(app)

# Before any requests are made, create data.db and all required tables, unless
# they already exist.
@app.before_first_request  # this is a Flask decorator
def create_tables():
    db.create_all()
    # can only create the tables it 'sees'. It's important to import
    # everything we need SQLAlchemy to see, and create tables for.
