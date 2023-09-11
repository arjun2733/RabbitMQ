import pika
from flask import Flask, request, jsonify
from pika.adapters.blocking_connection import BlockingChannel
import os

app = Flask(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection.channel()

def send_to_queue(channel: BlockingChannel, queue: str, message: str):
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)

@app.route('/health_check', methods=['GET'])
def health_check():
    message = request.args.get('message', 'Health Check')
    channel = get_rabbitmq_channel()
    send_to_queue(channel, 'health_check', message)
    return jsonify({'status': 'OK' , 'action' : 'health_check'})

@app.route('/insert_record/<SRN>/<Name>/<Section>', methods=['GET'])
def insert_record(SRN, Name, Section):
    record = {'SRN': SRN, 'Name': Name, 'Section': Section}
    channel = get_rabbitmq_channel()
    send_to_queue(channel, 'insert_record', str(record))
    return jsonify({'status': 'OK' , 'action' : 'insert_record'})


@app.route('/read_database', methods=['GET'])
def read_database():
    channel = get_rabbitmq_channel()
    send_to_queue(channel, 'read_database', '')
    return jsonify({'status': 'OK' , 'action' : 'read_database'})

@app.route('/delete_record', methods=['GET'])
def delete_record():
    srn = request.args.get('SRN')
    channel = get_rabbitmq_channel()
    send_to_queue(channel, 'delete_record', srn)
    return jsonify({'status': 'OK','action' : 'delete_record'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
