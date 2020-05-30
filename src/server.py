import asyncio
import threading

import websockets
import pika

from RabbitMQConsumerThread import RabbitMQConsumerThread
# from src.RabbitMQConsumerThread import RabbitMQConsumerThread

amqp_url = 'amqp://hiiscdyn:r82F2WHFvJ8cGyb6ZVabMbzvprfKk92O@rattlesnake.rmq.cloudamqp.com/hiiscdyn'


async def handle_client(websocket, path):
    # await matched id list from client
    print("[WebSocketServer] Client connected!")
    id_list = await websocket.recv()
    threads = []
    id_list = id_list.split(' ')
    # await websocket.send("message from handler")

    # subscribe to the queues for all the ids in the list
    for matched_contact_id in id_list:
        t = RabbitMQConsumerThread(websocket, matched_contact_id)
        # t = threading.Thread(target=rabbitmq_channel_subscription, args=(matched_contact_id, connections))
        threads.append(t)
        t.start()

    await websocket.wait_closed()

    print("[WebSocketServer] Client closed connection! Stopping all subscription threads...")
    for t in threads:
        t.stop()

    params = pika.URLParameters(amqp_url)
    connection_rabbitmq = pika.BlockingConnection(params)
    channel = connection_rabbitmq.channel()

    for matched_contact_id in id_list:
        channel.basic_publish(exchange='', routing_key=f"matched_contact_id_{matched_contact_id}",
                              body='end all connections msg')
    connection_rabbitmq.close()
    print("[WebSocketServer] Stopped all subscription threads. Client disconnect successful!")


server_host = "0.0.0.0"
server_port = 8765
start_server = websockets.serve(handle_client, port=server_port)
print("[WebSocketServer] Started server on port: ", server_port)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
