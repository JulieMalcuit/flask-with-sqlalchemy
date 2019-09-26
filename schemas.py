from wsgi import ma
from models import Product

class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name') # These are the fields we want in the JSON!

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


product_schema_only = ProductSchema()
products_schema_only = ProductSchema(many=False)


class Counter:
    def __init__(self):
        self.id = 3

    def next(self):
        self.id += 1
        return self.id

ID = Counter()
print(ID.next())
