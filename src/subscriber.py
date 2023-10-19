import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pika


rabbit_host = '10.128.0.13'
rabbit_user = 'monitoring_user'
rabbit_password = 'rasi'
exchange = 'monitoring_citas'
topics = ['citas.#']

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

for topic in topics:
    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=topic)

print('> Waiting measurements. To exit, press CTRL+C')


def callback(ch, method, properties, body):
    payload = json.loads(body.decode('utf8').replace("'", '"'))
    topic = method.routing_key.split('.')
    emit('measurement', {
        'variable_name': topic[2],
        'value': payload['value'],
        'unit': payload['unit'],
        'topic': topic[0] + topic[1]
    })

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()