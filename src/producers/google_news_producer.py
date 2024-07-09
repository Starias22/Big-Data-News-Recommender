from news_producer import NewsProducer
print('Producing news')
news_producer=NewsProducer()
news_producer.db_connection(db=1)
news_producer.run(source='google_news')
