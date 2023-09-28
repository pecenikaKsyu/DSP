## PAD - Distributed Systems Programming 
---
### Laboratory Work 1 
#### Online Shop for Clothes 

**Implemented by: Wu Xenia-Qin Li**

**Reviewed by: Maxim Volosenco**


---
#### Assesess Application Suitability 

**Scalability**
Microservices let each service grow separately if the demand for various components of application varies. For instance, during a sale, an e-commerce application can experience high traffic for product catalog updates but low traffic for checkouts.

**Flexibility and Agility**
Teams can work on various components of the application concurrently thanks to microservices, which accelerates development. Faster deployments result from changes to one microservice not necessarily having an impact on others.

**Technoogy Diversity**
Microservices makes possible to utilize the most suitable technology stack for each microservice, even if the application needs various programming languages or technologies for various components. Performance and development effectiveness could be enhanced by this.

**Fault Isolation**
By isolating errors to certain components, microservices can reduce the effect of failures. The entire application may not be impacted if one service fails. This may increase system dependability.


**Easy Maintenance**
It's simpler to maintain smaller codebases. Microservices reduce the overall complexity of the program by making it simpler to locate and resolve problems inside particular services.


**Team Independence**
Different development teams can operate on independent microservices thanks to microservices design, giving increased freedom and autonomy in decision-making. Teams can select the technology and solutions that are most suited for their unique tasks.


**Scaling Resources**
Resource allocation is made efficient through microservices. For instance, if processing images requires a lot of resources in application, it might devote extra resources to that particular microservice.


**Continuous Deployment**
Continuous integration and continuous deployment (CI/CD) procedures work well with microservices, allowing for quicker user delivery of new features and updates.


**Cost Eficiency**
Microservices can reduce the cost of the infrastructure. By allocating resources only as needed,over-provisioning for monolithic apps are avoided.


As an example could serve **Amazon**, which is an e-commerce platform that relies on microservices to handle various functions, from order processing to product recomentations. With this strategy, Amazon is able to maintain a high level of availability while adapting to shifting customer demands.

---
#### Define Service Boundaries

**User Authentification Microservice:** This microservice handles login, authentication, and user registration. User profiles and authentication tokens are managed by it.

**Product Catalog Microservice:** Product information management falls under the purview of the product catalog microservice. It keeps information about clothes, including names, descriptions, costs, and pictures. It may also have search and product classification features.

**Order Management Microservice:** The processing of orders is handled by this microservice. It deals with order history, order updates (such shipping status), and order creation. Based on the chosen products, it determines the overall cost of orders.

**Payment Gateway Microservice:** Even though it isn't specifically depicted in the diagram, it might have a different microservice in charge of processing payments. To enable safe and effective payment transactions, this service communicates with payment providers.

**Client:** The user interface that clients interact with is represented by the frontend. In order to show products, handle user authentication, and control the shopping cart, it makes API calls to the microservices.

```mermaid
graph LR
A[Client] --> B[Authentification MS]
B --> C[Product Catalog MS]
C --> D[Order Management MS]
D --> E[Payment Gateway MS]
E --> F[DataBase]
```

---
#### Choose Technology Stack and Communication Patterns 

**User Authentificaton Microservice** 

_Language:_ Python 

_Framework:_ Flask 

_Database:_ PostgreSQL

**Product Catalog Microservice** 

_Language:_ JavaScript (Node.js)

_Framework:_ Express.js for building RESTful APIs

_Database:_ MongoDB for storing information about the product (NoSQL database)

**Order Management Microservice** 

_Language:_ Python

_Framework:_ Flask or FastAPI for building RESTful APIs

_Database:_ PostgreSQL for storing order and user data (Relational database)

**Payment Gateway Microservice**

_Language:_ JavaScript

_Framework:_ Express.js

_Databese:_ PostgreSQL

**Communication Patterns**
The main communication pattern used in this project is request-response model. Message queues(RabbitMQ/Kafka) will assure asyncronous communication between the microservices. 

---

#### Data Design and Management 
**User Authentification Microservice** 
1. _Endpoint:_ `/register`
* Method: POST
* Data Sent (JSON): 
```json 
{
  "username": "user123",
  "password": "password123",
  "email": "user@example.com"
}
```
* Response (JSON): 
```json
{
  "message": "Registration successful."
}
```
2. _Endpoint:_ `/login`
* Method: POST
* Data Sent (JSON): 
```json 
{
  "username": "user123",
  "password": "password123",
}
```
* Response (JSON): 
```json
{
  "user_id": "123456789",
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

**Product Catalog Microservice**
1. _Endpoint:_ `/products`
* Method: GET
* Data Sent: None
* Response (JSON): 
```json
[
  {
    "product_id": "product123",
    "name": "T-shirt",
    "description": "Comfortable cotton T-shirt",
    "price": 19.99,
    "image_url": "https://example.com/tshirt.jpg"
  },
  {
    "product_id": "product456",
    "name": "Jeans",
    "description": "Classic denim jeans",
    "price": 39.99,
    "image_url": "https://example.com/jeans.jpg"
  }
]
```

2. _Endpoint:_ `/products/{product_id}`
* Method: GET
* Data Sent: None
* Response (JSON): 
```json
{
   "product_id": "product123",
   "name": "T-shirt",
   "description": "Comfortable cotton T-shirt", 
   "price": 19.99, 
   "image_url": "https://example.com/tshirt.jpg" 
}
```

**Order Management Microservice**
1. _Endpoint:_ `/orders`
* Method: POST
* Data Sent (JSON): 
```json 
{
  "user_id": "123456789",
  "products": [
    {
      "product_id": "product123",
      "quantity": 2
    },
    {
      "product_id": "product456",
      "quantity": 1
    }
  ]
}
```
* Response (JSON): 
```json
{
  "order_id": "order987",
  "total_price": 79.97
}
```

2. _Endpoint:_ `/orders/{order_id}`
* Method: GET
* Data Sent: None
* Response (JSON): 
```json
{
  "order_id": "order987",
  "user_id": "123456789",
  "products": [
    {
      "product_id": "product123",
      "name": "T-shirt",
      "quantity": 2
    },
    {
      "product_id": "product456",
      "name": "Jeans",
      "quantity": 1
    }
  ],
  "total_price": 79.97,
  "status": "processing"
}
```
---
##### Set Up Deployment and Scaling 
**Deployment**
1. _Containerization:_ Each microservice should be containerized using Docker. This guarantees consistency in the environments for development, testing, and production.


**Scaling**
1. _Horizontal Scaling:_ Run many instances of the same Docker container to manually scale the microservices. Simple Docker commands or container management tools can be used for this.

2. _Auto-Scaling:_ If it is used a container orchestration solution like Docker Swarm or Amazon ECS, it could be used auto-scaling feature. For instance, Docker Swarm can scale services automatically based on the required replica count or other factors.


3. _Load Balancing:_ Install a reverse proxy or load balancer in front of the microservices, such as Nginx or HAProxy. Microservices' various instances can receive incoming traffic via this load balancer. The load balancer can be set up to employ a least-connections or round-robin algorithm.
 
4. _Service Mesh:_ To monitor and regulate communication between microservices, take into consideration constructing a service mesh like Istio or Linkerd. This can help with monitoring, traffic routing, and load balancing.

5. _Caching:_ For data that is often accessed, use caching techniques to speed up response times and lessen the stress on databases.

6. _Database Scaling:_ Implement database scaling techniques, such as sharding, replication, or managed database services that provide automatic scalability.

7. _Monitoring and Alerts:_ Use performance metric collection and visualization software such as Prometheus and Grafana. Create alerts to receive notifications about any performance problems or unusual behavior.

8. _Logging and Tracing:_ To effectively identify and resolve problems, use distributed tracing and centralized logging.

9. _Fault Tolerance:_ When designing microservices, consider fault tolerance. Use circuit breakers, fallback plans, and retry methods to gracefully handle failures.

10. _Global Distribution:_ Consider employing Content Delivery Networks (CDNs) or microservice deployment in various areas if online clothes store caters to a global audience to reduce latency and enhance customer experience.
