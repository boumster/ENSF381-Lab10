"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
Name : server.py
Assignment : Lab 10 , Exercise A ,B , C
Author ( s ) : Phoenix Bouma, Victor Gouttin
Submission : May 21 , 2030
Description : Flask .
= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
"""


from flask import Flask, request, jsonify, send_from_directory

import json
import os

app = Flask(__name__)

def load_products():
    with open('products.json') as f:
        return json.load(f)['products']

@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        return jsonify(product) if product else ('', 404)

@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({'products': products}, f)
    return jsonify(new_product), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return ('', 404)
    id = product['id']
    product.update(request.json)
    product['id'] = id
    with open('products.json', 'w') as f:
        json.dump({'products': products}, f)
    return jsonify(product), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return ('', 404)
    products = [p for p in products if p['id'] != product_id]
    
    # Update the IDs of the remaining products
    for i, product in enumerate(products):
        product['id'] = i + 1
    
    with open('products.json', 'w') as f:
        json.dump({'products': products}, f)
    return ('', 204)

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

if __name__ == '__main__':
    app.run(debug=True)
