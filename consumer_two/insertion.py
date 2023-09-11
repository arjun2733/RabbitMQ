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

def insert_into_mongodb(collection, document):
    result = collection.insert_one(document)
    print(f"Inserted document into MongoDB: {result.inserted_id}")

def on_message(channel, method, properties, body):
    message = body.decode('utf-8')
    insert_into_mongodb(get_mongodb_collection(), {'message': message})
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue='insert_record')
    channel.basic_consume(queue='insert_record', on_message_callback=on_message)
    print("Waiting for insert record messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()
