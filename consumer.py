import pika
import json
# import os

from pprint import pprint

# AMQP_URI = os.getenv("AMQP_URI", "amqp://guest:guest@localhost:5672")
# connection_parameter = pika.URLParameters(AMQP_URI)

QUEUE_NAME = "worker"
connection_parameter = pika.ConnectionParameters(
    'localhost', heartbeat=600, blocked_connection_timeout=300, credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


def callback(ch, method, properties, body):
    print(f"Received in  queue_name: {QUEUE_NAME}")

    data = json.loads(body)
    payload = {
        "data": data,
        "channel": ch,
        "method": method,
        "properties": properties,
    }

    pprint(payload)

    if properties.content_type == 'created':
        print("created")
    elif properties.content_type == 'update':
        print("updated")
    elif properties.content_type == 'delete':
        print("deleted")


channel.basic_consume(
    queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("Started Consuming...")

channel.start_consuming()
