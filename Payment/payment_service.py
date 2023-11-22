from Payment.payment_cache import ConsistentHashing
from RedirectError import should_simulate_redirect_error
from RedirectError import RedirectError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pybreaker import CircuitBreaker

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment_database.db'  # SQLite database for simplicity
db = SQLAlchemy(app)

# Create a ConsistentHashing instance for payment service
payment_service_hashing = ConsistentHashing(nodes=["Server-A", "Server-B", "Server-C"])

# Define a Payment model
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending')

payments = []

def custom_fail_function(circuit, error):
    if isinstance(error, RedirectError):  
        return True  
    return False

circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=10, fail_function=custom_fail_function)

@app.route('/process_payment', methods=['POST'])
@circuit_breaker
def process_payment():
    data = request.get_json()
    order_id = data['order_id']
    amount = data['amount']
    payment_method = data['payment_method']

    responsible_server = payment_service_hashing.get_node(str(order_id))
    
    # Create a new payment record in the database
    new_payment = Payment(order_id=order_id, amount=amount, payment_method=payment_method)
    db.session.add(new_payment)
    try: 
        db.session.commit()
        return jsonify({'message':'Payment processed successfully'}), 201
    except Exception as e: 
        db.session.rollback()
        return jsonify({'message': 'Payment processing failed'}), 500

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