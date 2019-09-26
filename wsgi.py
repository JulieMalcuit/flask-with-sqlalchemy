import os
import logging
#logging.warn(os.environ["DUMMY"])

from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

from models import Product
from schemas import products_schema

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/products/<int:post_id>', methods=['GET'])
def read_product():
    read_product = db.session.query(Product).get(post_id)
    return products_schema.jsonify(read_product)
