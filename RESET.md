# RESET

## Drop Redis databases

```sh
redis-cli flushall
```

## Drop Mongodb `news_recommendation_db`

1. Open a mongo shell using mongosh

    ```sh
    mongosh
    ```

2. Switch to `news_recommendation_db`

   ```sh
   use news_recommendation_db
   ```

3. Drop the database

   ```sh
   db.dropDatabase()
   ```

## Start Zookeeper and Kafka server.

```sh
bin/zookeeper-server-start.sh config/zookeeper.properties
```

```sh
bin/kafka-server-start.sh config/server.properties
```

## Remove topics

1. You can list all the available topics

   ```sh
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
   ```

2. Now remove each topic

    ```sh
    bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic  RawNewsTopic
    ```
    
    ```sh
    bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic  FilteredNewsTopic
    ```
    
    ```sh
    bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic  ProcessedNewsTopic
    ```
    
     
    ```sh
    bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic  InteractionsTopic
    ```
## Recreate the topics and list them

```sh
    bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic RawNewsTopic --partitions 4 --replication-factor 1
```
 
   ```sh
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic FilteredNewsTopic --partitions 4 --replication-factor 1
   ```

   ```sh
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ProcessedNewsTopic --partitions 4 --replication-factor 1
   ```

  ```sh
  bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic InteractionsTopic --partitions 4 --replication-factor 1
  ```

   ```sh
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
   ```

## Remove checkpoint for stream processor

At the root directory of the project, run the following commmand

```sh
rm -rf checkpoint/
```

## Run the raw news stream processor

Run spark raw news stream processor.

The raw news stream processor

   - Gets news messages from **RawNewsTopic**
   - Filters the news to remove news without URL, content or description and also duplicate news
   - Sends the filtered news to **FilteredNewsTopic**
   - Preprocesses the filtered news by performing cleaning, tokennization, lemmatization and stopwords removal
   - Processes the preprocessed news by performing sentiment analysis, topic detection and categorization on the description field of the news
   - Send the processed news to **ProcessedNewsTopic**

```sh
   python3 raw_news_stream_processor.py
```

## Run news producers 

Keep the raw news stream processor running and open another window.

Run news producers to retrieve news using News API and Gooogle news and then send them to **RawNewsTopic**

Move to scr/producers and run the following commands

 ```sh
   python3 news_api_producer.py
```

 ```sh
   python3 google_news_producer.py
```

These news producers will send news messages to **RawNewsTopic**

As news messages arrivse, the raw news stream processor will be processing them.

## Run filtered news saver

Move to src/consumer and run filtered news saver.

This retrieves filtered news messages from **FilteredNewsTopic** and insert them into the collection **filtered_news** of the **news_recommendation_db** in MongoDB.

You can run the following command in mongosh to check the inserted filtered news

   1. Open a mongo shell using mongosh

   ```sh
   mongosh
   ```
   2. Switch to **news_recommendation_db**

   ```sh
    use news_recommendation_db
   ```

   3. Show the collections available

   ```sh
   show collections
   ```

   You should see `filtered_news` listed.

   4. List all filtered news

   ```sh
    db.filtered_news.find()
   ```

## Run the application

Move to the root directory of the project and execute the following command to run the application.

```sh
   streamlit run app.py
```

## Register a user

Register at least one user with a valid email address and confirm the verification code.

## Run processed news recommender

Move to src/consumer and run the following command.

```sh
python3 processed_news_recommender.py
```

The processed news recommender retrieves processed news messages from **ProcessedNewsTopic** and recommend them to each user in the users collection based on their preferences of categories, sentiments and similarities with already seen news.

## Navigate

Now go the the application web page, login to an user account created above and see the recommended news.
