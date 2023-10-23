const fetch = require('node-fetch');

// Consul agent address and port
const consulAgentAddress = 'http://localhost';
const consulAgentPort = 8500;

// Function to discover a service by name
async function discoverService(serviceName) {
  try {
    const response = await fetch(`${consulAgentAddress}:${consulAgentPort}/v1/catalog/service/${serviceName}`);
    const data = await response.json();

    if (data.length === 0) {
      throw new Error(`Service '${serviceName}' not found`);
    }

    // Retrieve the address and port of a healthy instance of the service
    const service = data[0];
    const { ServiceAddress, ServicePort } = service;

    return `http://${ServiceAddress}:${ServicePort}`;
  } catch (error) {
    throw new Error(`Error discovering service: ${error.message}`);
  }
}

// Example usage:
async function main() {
  try {
    const serviceName = 'order-service'; // Replace with the name of the service you want to discover

    const serviceEndpoint = await discoverService(serviceName);
    console.log(`Discovered service '${serviceName}' at ${serviceEndpoint}`);
  } catch (error) {
    console.error(error.message);
  }
}

main();
