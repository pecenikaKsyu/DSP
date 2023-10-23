const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

// Define the base URLs for the microservices
const orderServiceBaseUrl = 'http://localhost:5000';
const paymentServiceBaseUrl = 'http://localhost:5001';

// Middleware to parse JSON requests
app.use(express.json());

// Gateway endpoint to create an order
app.post('/create_order', async (req, res) => {
  try {
    // Forward the request to the Order Management Microservice
    const response = await axios.post(`${orderServiceBaseUrl}/create_order`, req.body);
    res.status(response.status).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error creating order' });
  }
});

// Gateway endpoint to process a payment
app.post('/process_payment', async (req, res) => {
  try {
    // Forward the request to the Payment Gateway Microservice
    const response = await axios.post(`${paymentServiceBaseUrl}/process_payment`, req.body);
    res.status(response.status).json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error processing payment' });
  }
});

// Start the gateway server
app.listen(port, () => {
  console.log(`Gateway listening on port ${port}`);
});
