from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary data store for orders (replace with a database in a production system)
orders = []

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    user_id = data['user_id']
    
    # Perform validation and processing here
    
    order = {
        'product_id': product_id,
        'quantity': quantity,
        'user_id': user_id,
    }
    
    orders.append(order)
    
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/get_orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders}), 200

if __name__ == '__main__':
    app.run(port=5000)
