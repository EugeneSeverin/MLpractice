from multiprocessing import Process
from fastapi import FastAPI
import uvicorn
import pika


app = FastAPI()

def start_api_server():

    uvicorn.run("app.app:app",
                host="127.0.0.1",
                port=8000,
                reload=True)
    
def producer_task(body: str):

    connection_producer = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection_producer.channel()
    
    channel.queue_declare(queue='hello')
    
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=body)
    
    connection_producer.close()

    
    print(f'[x] send {body}!')

def consumer_task():

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def print_hello(name):
    print(f'Hello, {name}!')

if __name__ == "__main__":
    p1 = Process(target=start_api_server)
    p2 = Process(target=print_hello, args=('Eugene',))
    p3 = Process(target=producer_task, args=('Hello, World!',))
    p4 = Process(target=consumer_task)


    p1.start()
    p3.start()
    p4.start()
    try:
        p1.join()  
    except:
        p3.terminate()
        p4.terminate()

