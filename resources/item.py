from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        
        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))

        # connection.commit()
        # connection.close()

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found.'}, 404

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item: 
            item.price = data['price']
            # try:
            #    updated_item.insert()
            # except:
            #     return {"message": "An error occurred inserting the item."}, 500
        else:
            item = ItemModel(name, data['price'], data['store_id'])
            # also works:
            # item = ItemModel(name, **data)
            # try:
            #     updated_item.insert()
            # except:
            #     return {"message": "An error occurred updating the item."}, 500
        
        item.save_to_db()

        return item.json()


class ItemList(Resource): # class should be separated by two new lines in a file - coding convention for Python
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})

        # connection.close()

        # return {'items': items}

        # also works: list comprehension
        # return {'items': [x.json() for x in ItemModel.query().all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
