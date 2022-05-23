import pika
import json

node = pika.URLParameters('amqp://guest:guest@10.10.31.177:5672')

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
connection = pika.BlockingConnection(node)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='likes', body=json.dumps(body), properties=properties)

test = {
    "test": "test"
}

publish('created', test)