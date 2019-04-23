from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):
    # return a specific store
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()  # no need for 200 code, as it's the default
        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        # store doesn't exist, create it
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500

        # saved to db successfully, return it
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
        # creates an array of json objects from every store in table
