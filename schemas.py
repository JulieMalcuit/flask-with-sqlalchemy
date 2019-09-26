from wsgi import ma
from models import Product

class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name') # These are the fields we want in the JSON!

product_schema = ProductSchema()  # python object -> json
products_schema = ProductSchema(many=True)  # list python objects -> json


