from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pika
import json

app = Flask(__name__)
socketio = SocketIO(app)

rabbit_host = '10.128.0.13'
rabbit_user = 'monitoring_user'
rabbit_password = 'rasi'
exchange = 'monitoring_citas'
topics = 'cita'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

for topic in topics:
    channel.queue_bind(
        exchange=exchange, queue=queue_name, routing_key=topic)

print('> Waiting citas. To exit, press CTRL+C')

@socketio.on('connect')
def handle_connect():
    print("Client connected")

def callback(ch, method, properties, body):
    try:
        payload = json.loads(body)
        topic = method.routing_key.split('.')
        emit('cita', payload)  # Emitir el payload JSON a los clientes conectados
        print("Measurement :%r" % (str(payload)))
    except json.JSONDecodeError:
        print("Error al decodificar el mensaje JSON:", body)
        

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

if __name__ == '__main__':
    socketio.run(app, debug=True)