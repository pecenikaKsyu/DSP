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

# Endpoint to retrieve a specific payment by payment ID
@app.route('/get_payment/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = next((p for p in payments if p.get('payment_id') == payment_id), None)
    if payment is None:
        return jsonify({'message': 'Payment not found'}), 404
    return jsonify(payment), 200

# Endpoint to refund a payment by payment ID
@app.route('/refund_payment/<int:payment_id>', methods=['POST'])
def refund_payment(payment_id):
    for payment in payments:
        if payment.get('payment_id') == payment_id:
            if payment.get('status') == 'completed':
                payment['status'] = 'refunded'
                return jsonify({'message': 'Payment refunded successfully'}), 200
            else:
                return jsonify({'message': 'Payment cannot be refunded as it is not completed'}), 400
    
    return jsonify({'message': 'Payment not found'}), 404

if __name__ == '__main__':
    app.run(port=5001)
