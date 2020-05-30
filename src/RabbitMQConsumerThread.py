import asyncio
import threading

import pika


class RabbitMQConsumerThread(threading.Thread):
    def __init__(self, websocket, matched_contact_id):
        super(RabbitMQConsumerThread, self).__init__()
        self._is_interrupted = False
        self.websocket = websocket
        self.matched_contact_id = matched_contact_id
        self.amqp_url = 'amqp://hiiscdyn:r82F2WHFvJ8cGyb6ZVabMbzvprfKk92O@rattlesnake.rmq.cloudamqp.com/hiiscdyn'

    def stop(self):
        self._is_interrupted = True

    def run(self):
        print(f"[RabbitMQConsumerThread] started rabbitmq consumer for matched contact id: {self.matched_contact_id}")
        params = pika.URLParameters(self.amqp_url)
        connection_rabbitmq = pika.BlockingConnection(params)

        channel = connection_rabbitmq.channel()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # delegate rabbitmq message back to websocket
        for message in channel.consume(f"matched_contact_id_{self.matched_contact_id}", auto_ack=True):
            if self._is_interrupted:
                break
            if not message:
                continue
            method, properties, body = message
            print(f"[RabbitMQConsumerThread] Received rabbitmq message: {body} on message_id: {self.matched_contact_id}")
            asyncio.get_event_loop().run_until_complete(self.send_message_on_ws(body))
        connection_rabbitmq.close()

    async def send_message_on_ws(self, message):
        print(f"[RabbitMQConsumerThread] Sending message on websocket: {message}")
        await self.websocket.send(message)
