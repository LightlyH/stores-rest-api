from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id): # constructor
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone() # unique row
        # connection.close()

        # if row:
        #     # return cls(row[0], row[1]) # call the constructor and build a new ItemModel object 
        #     return cls(*row) # the same as above, using argument unpacking
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()

    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.name, self.price))

    #     connection.commit()
    #     connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()