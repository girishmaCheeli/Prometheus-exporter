How It Works
Environment Variables:

RABBITMQ_HOST: RabbitMQ hostname (default: localhost).
RABBITMQ_USER: RabbitMQ username (default: guest).
RABBITMQ_PASSWORD: RabbitMQ password (default: guest).
SCRAPE_INTERVAL: Time interval (in seconds) to scrape RabbitMQ metrics (default: 15).
RabbitMQ HTTP API:

The script queries the /api/queues endpoint to fetch queue information.
It uses HTTP Basic Authentication (requests.get with auth=(username, password)).
Prometheus Metrics:

Three metrics are exposed:
rabbitmq_individual_queue_messages
rabbitmq_individual_queue_messages_ready
rabbitmq_individual_queue_messages_unacknowledged
Each metric is labeled with host, vhost, and name.
Prometheus HTTP Server:

The exporter runs an HTTP server on port 8000 (default for Prometheus exporters) to expose metrics.
Error Handling:

Catches and logs exceptions when the RabbitMQ API is unreachable or returns an error.
