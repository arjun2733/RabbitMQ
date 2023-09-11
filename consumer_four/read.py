import pika
import pymongo
import os
import time
time.sleep(20)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
MONGODB_HOST = 'mongodb'

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection.channel()

def get_mongodb_collection():
    client = pymongo.MongoClient(
        host=MONGODB_HOST,
        port=27017,
        username='root',
        password='cc_project',
        authSource='admin',
        authMechanism='SCRAM-SHA-256'
    )
    db = client['studentdb']
    collection = db['student']
    return collection

def read_mongodb(collection, document):
    res = collection.find({})
    for document in res:
        print(document)
    print(f"Read document in MongoDB")

def on_message(channel, method, properties, body):
    message = body.decode('utf-8')
    read_mongodb(get_mongodb_collection(), {'message': message})
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue='read_database')
    channel.basic_consume(queue='read_database', on_message_callback=on_message)
    print("Waiting for read database messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()
