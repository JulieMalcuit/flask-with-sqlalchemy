import os
import logging
#logging.warn(os.environ["DUMMY"])

from flask import Flask, request, abort
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

@app.route('/')
def hello():
    return "Hello World!"
from models import Product
from schemas import products_schema

@app.route('/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

from schemas import product_schema

@app.route('/products/<int:post_id>', methods=['GET'])
def read_product(post_id):
    product = db.session.query(Product).get(post_id)
    return product_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def add_product():
    product = Product()
    body = request.get_json()
    product.name = body["name"]
    db.session.add(product)
    db.session.commit()
    return "", 201

@app.route('/products', methods=['PATCH'])
def update_product(post_id):
    product = Product()
    body = request.get_json()
    db.session.query(Product).filter(Product.id == post_id).\
        update({product.name: body["name"]}, synchronize_session=False)
    db.session.add(product)
    db.session.commit()
    return "", 204

@app.route('/products', methods=['POST'])
def delete_product(post_id):
    pass
