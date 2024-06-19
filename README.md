
# Big Data News Recommender

## Description

The Big Data News Recommender is a system designed to provide personalized news recommendations using big data technologies. It processes large streams of news articles and user interaction data to suggest relevant news content to users.

## Table of Contents

- [Installation](#installation)
- [Kafka Setup](#kafka-setup)
- [Usage](#usage)
- [Pipeline Overview](#pipeline-overview)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Acknowledgments](#acknowledgments)

## Installation

### Prerequisites
- A Linux distribution
- Python 3.x
- pip

Check installation
```sh
pip --version
```
If not installed, install it

```sh
sudo apt install python3-pip
```

- Java >= 8

Check installation
```sh
java -version
```
If not installed, install it
```sh
sudo apt install openjdk-21-jdk
```

Set Java 21 as default and configure JAVA_HOME
```sh
sudo update-alternatives --config java
nano .bashrc
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64/
source .bashrc
echo $JAVA_HOME
```

- Redis

Install Redis
```sh
sudo apt install curl
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install redis
```

- Virtual Environment (recommended)

Install venv for virtual environments.
```sh
sudo apt install python3-venv
```

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Starias22/Big-Data-News-Recommender.git
   cd Big-Data-News-Recommender
   ```

2. **Set up the virtual environment:**

   ```sh
   python3 -m venv big_data_env
   source big_data_env/bin/activate 
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Download the models folder:**

   Download the models zip file from [my drive](https://drive.google.com/drive/folders/1xyo_IqACn7A9cOo8sq9H2FeBptWwPM8y?usp=drive_link), unzip it, and put the extracted folder in the current working directory (the repository).

5. **Generate a NewsAPI key:**

   Generate a NewsAPI key [here](https://newsapi.org/register) and save it.

6. **Set up your config.json file:**

   Rename the file `config/config_template.json` to `config/config.json` and replace the value of the key "news_api_key" with the key you generated.

## Kafka Setup

### Steps

1. **Download Kafka:**

   ```sh
   wget https://downloads.apache.org/kafka/3.7.0/kafka-3.7.0-src.tgz
   ```

2. **Extract Kafka:**

   ```sh
   tar -xvf kafka-3.7.0-src.tgz
   cd kafka-3.7.0-src
   ```

3. **Build Kafka:**

   ```sh
   ./gradlew jar -PscalaVersion=2.13.12
   ```

4. **Start Zookeeper:**

   ```sh
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

5. **Start Kafka:**

   ```sh
   bin/kafka-server-start.sh config/server.properties
   ```

6. **Create Kafka topics:**

   ```sh
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic RawNewsTopic --partitions 4 --replication-factor 1
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic FilteredNewsTopic --partitions 4 --replication-factor 1
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ProcessedNewsTopic --partitions 4 --replication-factor 1
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic InteractionsTopic --partitions 4 --replication-factor 1
   bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
   ```

## Usage

### Run the raw news stream processor

Run the Spark raw news stream processor.

```sh
run_spark_raw_news_stream_processor
```

### Run news producers

```sh
cd src/producers
python3 news_api_producer.py
python3 google_news_producer.py
```

### Run filtered news saver

```sh
cd src/consumer
run_filtered_news_saver
```

### Run the application

```sh
cd Big-Data-News-Recommender
streamlit run app.py
```

### Register a user

Register at least one user with a valid email address and confirm the verification code.

### Run processed news recommender

```sh
cd src/consumer
python3 processed_news_recommender.py
```

### Navigation

Log in to a user account and see the recommended news.

## Pipeline Overview

### Schema

```plaintext
        +---------------------+               +-----------------------+               +----------------------+               +----------------------+
        |  News Producers     |  ------->     |   Raw News Stream     |  ------->     |  Filtered News Saver |  ------->     | Processed News       |
        |  (NewsAPI, Google)  |               |   Processor           |               |                      |               | Recommender          |
        +---------------------+               +-----------------------+               +----------------------+               +----------------------+
                  |                                      |                                    |                                   |
                  |                                      |                                    |                                   |
                  v                                      v                                    v                                   v
        +---------------------+               +-----------------------+               +----------------------+               +----------------------+
        |   RawNewsTopic      |               |   FilteredNewsTopic   |               |   ProcessedNewsTopic |               | Recommendations to    |
        +---------------------+               +-----------------------+               +----------------------+               | User Profiles         |
                                                                                                                            +----------------------+
```

### Detailed Description

1. **News Producers**:
    - **Sources**: News articles are fetched from various sources such as NewsAPI and Google News.
    - **Kafka Topic**: These news articles are published to the `RawNewsTopic` Kafka topic.

2. **Raw News Stream Processor**:
    - **Task**: The processor reads raw news from the `RawNewsTopic`, filters out articles without URLs, content, or descriptions, and removes duplicates.
    - **Output**: Filtered news is then published to the `FilteredNewsTopic`.
    - **Preprocessing**: Additionally, it performs text preprocessing such as cleaning, tokenization, lemmatization, and stopwords removal.
    - **Processing**: It conducts sentiment analysis, topic detection, and categorization of the news articles.
    - **Kafka Topic**: Processed news articles are published to the `ProcessedNewsTopic`.

3. **Filtered News Saver**:
    - **Task**: This component consumes messages from the `FilteredNewsTopic` and saves the filtered news articles to a MongoDB collection `filtered_news`.

4. **Processed News Recommender**:
    - **Task**: This component consumes messages from the `ProcessedNewsTopic` and generates personalized news recommendations for users based on their preferences (categories, sentiments) and similarities with previously seen news.
    - **Output**: Recommendations are then sent to each user's profile, making them available for viewing on the application.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

Please make sure your code follows our coding guidelines and includes tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact Information

For questions or issues, please contact:

- Name: Gbètoho Ezéchiel ADEDE
- Email: Gbetoho.ADEDE@um6p.ma
- GitHub: [Starias22](https://github.com/Starias22)
- LinkedIn: [Gbètoho Ezéchiel ADEDE](https://www.linkedin.com/in/Starias22)

## Acknowledgments

- Thanks to [contributor1](https://github.com/contributor1) for their valuable input.
