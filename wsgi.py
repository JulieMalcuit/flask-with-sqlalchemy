from flask import Flask, request, abort, render_template
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def home():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/<int:id>')
def product_html(id):
    product = db.session.query(Product).get(id)
    return render_template('product.html', product=product)

@app.route('/products', methods=['GET'])  # GET / products
def read_products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def create_product():
    product = Product()
    body = request.get_json()

    # Test en version condensee
    # filtered_body = { key, value for key, value in body if key in ["name","description"]}
    #product = Product(**filtered_body)

    name = body.get("name") # Test dans le body que name existe
    if name is not None:
        product.name = name

    description = body.get("description")   # Test dans le body que la description existe
    if description is not None:
        product.description = description

    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product_to_delete = db.session.query(Product).get(id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return "", 204

@app.route('/products/<int:id>', methods=['PATCH'])
def update_product(id):
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")

    if name is None and description is None:
        abort(400)

    db.session.query(Product).filter(Product.id == id).update({
        Product.name: body["name"],
        Product.description: body["description"]
    })
    db.session.commit()
    return '', 204
