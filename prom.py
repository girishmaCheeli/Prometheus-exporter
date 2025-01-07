# prometheus-exporter
import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables for RabbitMQ connection
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "15"))

# Metrics
queue_messages = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total count of messages in a RabbitMQ queue",
    ["host", "vhost", "name"],
)
queue_messages_ready = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Count of ready messages in a RabbitMQ queue",
    ["host", "vhost", "name"],
)
queue_messages_unacknowledged = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Count of unacknowledged messages in a RabbitMQ queue",
    ["host", "vhost", "name"],
)

def fetch_queue_metrics():
    """Fetch metrics from RabbitMQ HTTP API and update Prometheus gauges."""
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    try:
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        queues = response.json()
        
        for queue in queues:
            host = RABBITMQ_HOST
            vhost = queue["vhost"]
            name = queue["name"]
            
            # Update Prometheus metrics
            queue_messages.labels(host=host, vhost=vhost, name=name).set(queue.get("messages", 0))
            queue_messages_ready.labels(host=host, vhost=vhost, name=name).set(queue.get("messages_ready", 0))
            queue_messages_unacknowledged.labels(host=host, vhost=vhost, name=name).set(queue.get("messages_unacknowledged", 0))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RabbitMQ metrics: {e}")

def main():
    """Main function to start the exporter."""
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("Prometheus exporter running on port 8000")
    
    # Periodically fetch and update metrics
    while True:
        fetch_queue_metrics()
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    main()

