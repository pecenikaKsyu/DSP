const express = require('express');
const axios = require('axios');

const app = express();
const port = 3002;

// In-memory store to keep track of registered services
const registeredServices = {};

app.use(express.json());

// Register a service with the service discovery
app.post('/register', (req, res) => {
  const { serviceId, serviceName, serviceHost, servicePort } = req.body;

  if (!serviceId || !serviceName || !serviceHost || !servicePort) {
    return res.status(400).json({ error: 'Invalid service registration data' });
  }

  // Store the service information
  registeredServices[serviceId] = {
    serviceName,
    serviceHost,
    servicePort,
  };

  return res.status(201).json({ message: 'Service registered successfully' });
});

// Discover a service by service ID
app.get('/discover/:serviceId', async (req, res) => {
  const { serviceId } = req.params;

  const serviceInfo = registeredServices[serviceId];

  if (serviceInfo) {
    try {
      const fetchModule = await import('node-fetch');
      const fetch = fetchModule.default;
      
      const response = await fetch(`${serviceInfo.serviceHost}:${serviceInfo.servicePort}/api/endpoint`);
      const data = await response.json();

      res.json(data);
    } catch (error) {
      res.status(500).json({ error: 'Error fetching data from the service' });
    }
  } else {
    return res.status(404).json({ error: 'Service not found' });
  }
});

app.listen(port, () => {
  console.log(`Service Discovery is running on port ${port}`);
});
