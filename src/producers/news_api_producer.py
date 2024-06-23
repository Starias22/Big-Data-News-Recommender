from news_producer import NewsProducer
news_producer=NewsProducer()


news_producer.db_connection(db=0)
news_producer.run(source='newsapi')