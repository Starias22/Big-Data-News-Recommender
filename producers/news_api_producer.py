from news_producer import NewsProducer
news_api_producer=NewsProducer(db=0)
news_api_producer.run(source='newsapi')