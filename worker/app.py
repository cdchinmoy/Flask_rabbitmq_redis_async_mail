import pika
import time
import mail_fire
import os

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(10)

print(' [*] Connecting to server ...')

credentials = pika.PlainCredentials(os.environ['RABBITMQ_USER'], os.environ['RABBITMQ_PASS'])
parameters =  pika.ConnectionParameters(os.environ['RABBITMQ_HOST'], credentials=credentials, heartbeat=5)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    print(" [x] Received %s" % body)
    cmd = body.decode('utf-8')
    print(cmd)
    mail_fire.send_mail(cmd)

    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()