import pika

amqp_url = 'amqp://hiiscdyn:r82F2WHFvJ8cGyb6ZVabMbzvprfKk92O@rattlesnake.rmq.cloudamqp.com/hiiscdyn'


params = pika.URLParameters(amqp_url)
connection_rabbitmq = pika.BlockingConnection(params)

channel = connection_rabbitmq.channel()

matched_contact_id = '1'
channel.basic_publish(exchange='', routing_key=f"matched_contact_id_{matched_contact_id}", body='acesta este un mesah frumos')
print ("[x] Message sent to consumer")
connection_rabbitmq.close()