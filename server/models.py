from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    # Ensure the relationship with reviews is correctly defined
    reviews = db.relationship('Review', back_populates='customer')

    # Ensure serialization rules exclude reviews.customer to avoid recursion
    serialize_rules = ('id', 'name', '-reviews.customer')

    # Define association proxy to get items through reviews
    items = association_proxy('reviews', 'item')

    # Define serialization rules
    serialize_rules = ('id', 'name', '-reviews.customer')  # Exclude reviews.customer
    
    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Float)

    # Define relationship with reviews
    reviews = db.relationship('Review', back_populates='item')

    # Define serialization rules
    serialize_rules = ('id', 'name', 'price', '-reviews.item')  # Exclude reviews.item
    
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Define relationship with Customer
    customer = db.relationship('Customer', back_populates='reviews')

    # Define relationship with Item
    item = db.relationship('Item', back_populates='reviews')
    
    # Define serialization rules
    serialize_rules = ('id', 'comment', 'customer_id', 'item_id', '-customer.reviews', '-item.reviews')  # Exclude customer.reviews and item.reviews
    
    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'

