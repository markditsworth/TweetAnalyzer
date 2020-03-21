from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_server=["localhost:29092"])

producer.send('my-topic',b'message').get()
