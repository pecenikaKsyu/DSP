import unittest
from order_service import app, db, Order

class TestOrderService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_create_order(self):
        data = {
            'product_id': 1,
            'quantity': 5,
            'user_id': 123
        }
        response = self.app.post('/create_order', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_orders(self):
        response = self.app.get('/get_orders')
        self.assertEqual(response.status_code, 200)

    def test_get_order(self):
        order = Order(product_id=1, quantity=5, user_id=123)
        db.session.add(order)
        db.session.commit()
        response = self.app.get('/get_order/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('product_id', response.json)
        self.assertEqual(response.json['product_id'], 1)

    def test_update_order(self):
        order = Order(product_id=1, quantity=5, user_id=123)
        db.session.add(order)
        db.session.commit()
        data = {'status': 'shipped'}
        response = self.app.put('/update_order/1', json=data)
        self.assertEqual(response.status_code, 200)
        updated_order = Order.query.get(1)
        self.assertEqual(updated_order.status, 'shipped')

if __name__ == '__main__':
    unittest.main()
