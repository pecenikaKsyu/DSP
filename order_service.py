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

# Endpoint to retrieve a specific order by order ID
@app.route('/get_order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = next((o for o in orders if o.get('order_id') == order_id), None)
    if order is None:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify(order), 200

# Endpoint to update the status of an order by order ID
@app.route('/update_order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    new_status = data.get('status')
    
    for order in orders:
        if order.get('order_id') == order_id:
            order['status'] = new_status
            return jsonify({'message': 'Order status updated'}), 200
    
    return jsonify({'message': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
