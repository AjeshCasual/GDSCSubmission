from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app)

@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    product_id = mongo.db.products.insert(data)
    return jsonify(str(product_id)), 201

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    mongo.db.products.update_one({'_id': id}, {"$set": data})
    return jsonify({'result': 'Product updated successfully'}), 200

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = mongo.db.products.find_one({'_id': id})
    return dumps(product), 200

@app.route('/product/<id>/variant', methods=['POST'])
def add_variant(id):
    data = request.get_json()
    product = mongo.db.products.find_one({'_id': id})
    if 'variants' in product:
        product['variants'].append(data)
    else:
        product['variants'] = [data]
    mongo.db.products.update_one({'_id': id}, {"$set": product})
    return jsonify({'result': 'Variant added successfully'}), 201

@app.route('/')
def home():
    return "Hello, Varianters!"


if __name__ == '__main__':
    app.run(debug=True)
