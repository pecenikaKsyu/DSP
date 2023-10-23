from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary data store for payments (replace with a payment gateway integration in a production system)
payments = []

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    order_id = data['order_id']
    amount = data['amount']
    payment_method = data['payment_method']
    
    # Perform payment processing here (integration with a real payment gateway)
    
    payment = {
        'order_id': order_id,
        'amount': amount,
        'status': 'completed'  # In a real system, check the payment status from the payment gateway
    }
    
    payments.append(payment)
    
    return jsonify({'message': 'Payment processed successfully'}), 201

@app.route('/get_payments', methods=['GET'])
def get_payments():
    return jsonify({'payments': payments}), 200

if __name__ == '__main__':
    app.run(port=5001)
