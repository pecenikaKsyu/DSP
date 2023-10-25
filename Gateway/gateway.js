const express = require('express');
const axios = require('axios');
const NodeCache = require('node-cache');

const app = express();
const port = 3000;

const orderServiceUrls = [
  'http://order-service-replica-1:5000',
  'http://order-service-replica-2:5000',
  'http://order-service-replica-3:5000',
  'http://order-service-replica-4:5000',
];

const paymentServiceUrls = [
  'http://payment-service-replica-1:5001',
  'http://payment-service-replica-2:5001',
  'http://payment-service-replica-3:5001',
  'http://payment-service-replica-4:5001',
];

let orderServiceIndex = 0;
let paymentServiceIndex = 0;

const cache = new NodeCache({ stdTTL: 60 });

function roundRobin(arr, currentIndex) {
  currentIndex = (currentIndex + 1) % arr.length;
  return currentIndex;
}

app.get('/get_orders', async (req, res) => {
  try {
    const orderServiceUrl = orderServiceUrls[orderServiceIndex];
    orderServiceIndex = roundRobin(orderServiceUrls, orderServiceIndex);

    const cacheKey = 'get_orders'; // Define a cache key
    const cachedData = cache.get(cacheKey);

    if (cachedData) {
      // Serve data from the cache if available
      res.json(cachedData);
    } else {
      const response = await axios.get(`${orderServiceUrl}/get_orders`);
      const data = response.data;

      // Cache the data for future requests
      cache.set(cacheKey, data);

      res.json(data);
    }
  } catch (error) {
    res.status(500).json({ error: 'Error fetching data from the order service' });
  }
});

app.get('/process_payment', async (req, res) => {
  try {
    const paymentServiceUrl = paymentServiceUrls[paymentServiceIndex];
    paymentServiceIndex = roundRobin(paymentServiceUrls, paymentServiceIndex);

    const cacheKey = 'process_payment'; // Define a cache key
    const cachedData = cache.get(cacheKey);

    if (cachedData) {
      // Serve data from the cache if available
      res.json(cachedData);
    } else {
      const response = await axios.get(`${paymentServiceUrl}/process_payment`);
      const data = response.data;

      // Cache the data for future requests
      cache.set(cacheKey, data);

      res.json(data);
    }
  } catch (error) {
    res.status(500).json({ error: 'Error processing payment' });
  }
});

app.listen(port, () => {
  console.log(`Gateway is running on port ${port}`);
});
