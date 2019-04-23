from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

'''
The Item resource - best practice is for a resource to contain
only methods that the API interacts with. e.g. find_by_name()
was in this Resource but has been moved to ItemModel.
'''


class Item(Resource):

    # class Item inherits from Resource
    # basic example of a 'resource'
    # any 'resource' Api works with, has to be a class
    # note: resources are usually mapped to database tables too

    parser = reqparse.RequestParser()

    # Request parsing - ensures only certain fields can be passed to
    # resources though JSON payload. reqparse can examine incoming
    # json payload, or html form payloads.
    # parser will parse payload with below args, i.e. 'price'.
    # It will not accept keys not specified in args

    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Every item needs a price."
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required()  # decorator forces authentication before get carried out
    def get(self, name):
        # use new find_by_name() class method
        item = ItemModel.find_by_name(name)
        if item:
            # call ItemModel()'s new json() method.
            # can't return an ItemModel object to client via API
            return item.json()
        # otherwise return error
        return {'message': "Item not found."}, 404

    @jwt_required()
    def post(self, name):
        # FIRST check if an item with that name already exists
        # since we want unique names
        if ItemModel.find_by_name(name):
            return {'message':
                    "an item with name {} already exists.".format(name)}, 400
            # http status code 400 is 'bad request'. Why bad?
            # client should have checked if item existed first

        # THEN parse request payload - why load before above check if it fails.
        # this is 'error first' approach.
        data = Item.parser.parse_args()

        # create an ItemModel instance
        item = ItemModel(name, **data)
        # **data equivalent to data['price'], data['store_id']

        # try insert item into db by calling ItemModel's insert() method
        try:
            item.save_to_db()  # since item is now an instance of ItemModel
        except:
            return {'message': 'An error occured inserting the item.'}, 500
            # 500 - internal server error

        return item.json(), 201  # confirming, 201 is status code for 'created'
        # a similar status code is 202 for accepted, but might take a while

    @jwt_required()
    def put(self, name):

        # http put request should either update an existing entry
        # or create one if it doesn't exist.

        # load / parse data first this time, since PUT uses data in both cases
        # i.e. item already exists, item doesn't exist.
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)  # instance of ItemModel

        if item is None:
            item = ItemModel(name, **data)
            # **data equivalent to data['price'], data['store_id']
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # a list comprehension that queries all items in ItemModel and packs
        # into json with our own json() method
        # i.e. get all items and iterate over them with json()
        # OR lamda function:
        #
        # return {'items': list(map(lamda x: x.json(), ItemModel.query.all()))}
        #
        # note: the list comprehension method is more 'pythonic', and arguably
        # more readable, and possible more performant.
        #
        # however, using list() and map() is better if you're programming in
        # multiple languages, or working with devs who use other languages.
