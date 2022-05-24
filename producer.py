from time import sleep
import pika
import json
# import os
import random

# AMQP_URI = os.getenv("AMQP_URI", "amqp://guest:guest@localhost:5672")
# connection_parameter = pika.URLParameters(AMQP_URI)

QUEUE_NAME = "worker"
connection_parameter = pika.ConnectionParameters(
    'localhost', heartbeat=600, blocked_connection_timeout=300, credentials=pika.PlainCredentials('guest', 'guest'))
connection = pika.BlockingConnection(connection_parameter)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


def publish(method, body):
    print(method)
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="",
                          routing_key=QUEUE_NAME,
                          body=json.dumps(body),
                          properties=properties)


try:
    while True:
        payload = {
            "number":  random.randint(1, 10)
        }
        publish("created", payload)
        print(f"send message: {payload}")
        sleep(1)
except Exception as e:
    channel.close()
    connection.close()
