# import sqlite3 so User class can interact with db
import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
    '''
    making this a Resource so we can add it to the API using
    Flask-Restful. Used by /register endpoint.
    A Resource is the external representation of an entity,
    whereas a model is our internal representation of the
    entity.
    '''

    # init a rreparse parser
    parser = reqparse.RequestParser()

    # tell it how to parse the incoming json
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank."
    )

    def post(self):
        # call on parser to parse request json
        data = UserRegister.parser.parse_args()

        '''
        check that requested username doesn't already exist
        using our existing find_by_user() method of User class
        SO, the UserRegister Resource is using a method of our
        User model. An example of where the two interact.
        '''
        if UserModel.find_by_username(data['username']):
            return{'message': "A user with that username already exists."}, 400

        user = UserModel(**data)  # **data - unpack data to args
        # user = UserModel(data['username'], data['[password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201  # created
