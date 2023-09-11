import pika
import os
import time
time.sleep(20)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

def get_rabbitmq_channel():
    print("RABBITMQ",RABBITMQ_HOST)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))
    return connection.channel()

def on_message(channel, method, properties, body):
    print(f"Health check message received: {body.decode('utf-8')}")
    channel.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel = get_rabbitmq_channel()
    channel.queue_declare(queue='health_check')
    channel.basic_consume(queue='health_check', on_message_callback=on_message)
    print("Waiting for health check messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()
