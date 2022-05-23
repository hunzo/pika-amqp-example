import pika
import json

from pprint import pprint

node = pika.URLParameters('amqp://guest:guest@10.10.31.177:5672')

connection = pika.BlockingConnection(node)
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='likes')


def callback(ch, method, properties, body):
    print("Received in likes...")
    print(body)
    data = json.loads(body)

    pprint(f'data: {data}')
    pprint(f'ch: {ch}')
    pprint(f'method: {method}')
    pprint(f'properties: {properties}')

    if properties.content_type == 'created':
        print("created")
    elif properties.content_type == 'update':
        print("updated")
    elif properties.content_type == 'delete':
        print("deleted")


channel.basic_consume(
    queue='likes', on_message_callback=callback, auto_ack=True)

print("Started Consuming...")

channel.start_consuming()
