
# Big Data News Recommender

## Description

The Big Data News Recommender is a system designed to provide personalized news recommendations using big data technologies. It processes large streams of news articles and user interaction data to suggest relevant news content to users.

## Table of Contents

- [Installation and Configurations](#installation-and-onfigurations)
  - [Prerequisites](#prerequisites)
  - [Clone the repository](#clone-the-repository)
  - [Download the trained models folder](#download-the-trained-models-folder)
  - [Download the necessary NLTK data](#download-the-necessary-nltk-data)
  - [Generate a NewsAPI key](#generate-a-newsapi-key)
  - [Email configuration](#email-configuration)
  - [Secret JSON file configuration](#secret-json-file-configuration)
  - [Docker compose file configuration](#docker-compose-file-configuration)
  - [Create Necessary Directories](#create-necessary-directories)
  - [Set Permissions](#set-permissions)
  - [Initialize Airflow](#initialize-airflow)
  - [Start All Services](#start-all-services)
  - [Access Kafka and create topics](#access-kafka-and-create-topics)
- [Usage](#usage)
  - [Run the raw news stream processor](#run-the-raw-news-stream-processor)
  - [Run raw news consumer](#run-raw-news-consumer)
  - [Run news producers](#run-news-producers)
  - [Run filtered news saver](#run-filtered-news-saver)
  - [Run the application](#run-the-application)
  - [Register a user](#register-a-user)
  - [Run processed news recommender](#run-processed-news-recommender)
  - [Navigation](#navigation)
- [Pipeline Overview](#pipeline-overview)
  - [Schema](#schema)
  - [Detailed Description](#detailed-description)
- [Reset](#reset)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)
- [Acknowledgments](#acknowledgments)

## Installation and Configurations

### Prerequisites
#### A Linux distribution
#### Python 3.x
#### pip
#### Docker and Docker Compose

### Clone the repository

   ```sh
   git clone https://github.com/Starias22/Big-Data-News-Recommender.git
   cd Big-Data-News-Recommender
   ```

### Download the trained models folder
   
Download the `trained_models` zip file  from  [my drive](https://drive.google.com/drive/folders/1qI7ojkrH3gJ3DySCI0V8ol_6k4VqXy8c?usp=sharing) , unzip it and put the extracted folder  in the current working directory(the repository)

### Download the necesssary NLTK data

NLTK is used to process the news description. You need to download the necessasy NLTK data. But firstly, NLTK needs to be installed.

1. **Set up a virtual environment:**

   ```sh
   python3 -m venv big_data_env
   source big_data_env/bin/activate 
   ```

2. **Install NLTK:**

   ```sh
   pip install nltk
   ```

3. **Download NLTK data:**

Run the following command to download the necessary NLTK data.

```python3
python3 download_nltk_data.py
```

You should have the necessary NLTK data downloaded into `nltk_data` folder of the project root.

4. **Check the downloaded data**

```bash
ls nltk_data/
```
You should see `corpora` and `sentiment` folders in the `nltk_data` folder.



### Generate a NewsAPI key

You need a NewsAPI key. You can generate one [here](https://newsapi.org/register).

After filling the requested information you will have a new key generated. Copy and paste it in a safe place.


### Email configuration

You need to configure a Google email address. This email address will be used to send One Time Password to users during registration. It will also be used by Airflow for email sending at the end of each task.

You have to create an app password. You can follow [this tutorial](https://itsupport.umd.edu/itsupport?id=kb_article_view&sysparm_article=KB0015112) to do it.

By the end of this step, you should have an app password created. Copy and store it in a safe place.


### Secret JSON file configuration

You need to configure your secret.json file.

First of all make a copy of the secret JSON template

```bash
cp config/secret_template.json config/secret.json
```

In the `secret.json` file replace the value of  the

- `newsapi_key`  field by the NewsAPI key you've generated above.

- `sender_address` field by the Google email address you used to generate app password in the previous step

- `password` field by the app password you've generated in the above

- `admin_email` field by the admin email. The admin email is the mail address airflow send task execution informations to using the `sender_address`  Google email address. 

### Kafka-ui config file

You need to personalize the Kafka UI config file. This is required by the Kafka UI to work.

First of all make a copy of the `kafka-ui/config_template.yml`.

```bash
cp kafka-ui/config_template.yml kafka-ui/config.yml
```

Then set your username and password in the `kafka-ui/config.yml`. You will use them to sign in into Kaka UI.

### Docker compose file configuration

You need to configure your `docker-compose.yml` file.

- First of all make a copy of the docker compose template

```bash
cp docker-compose-template.yml docker-compose.yml
```

- Open the `docker-compose.yml` file 

- Go to the  the airlow environment block ie 

`x-environment: &airflow_environment` and replace

1. the value of the `AIRFLOW__SMTP__SMTP_USER` and `AIRFLOW__SMTP__SMTP_MAIL_FROM` variables by the Google email address, your email sender address

2. the value of the `AIRFLOW__SMTP__SMTP_MAIL_FROM` variable by the app password you've generated


- Go to the  the airlow initialization service  ie 

`airflow-init` and replace the email address by the admin email address. Use the same email address as the value you set for  `admin_email` during the configuration of `the secret.json` file.

You should also set your username and password.

You may also want to set your firstname and lastname.

#### Create Necessary Directories

First, create a `data` directory and navigate into it. Within the `data` directory, create subdirectories for Zookeeper, Kafka brokers, checkpoints, Redis, PostgreSQL, and MongoDB. Additionally, create a directory for Airflow logs.

```bash
# Create the main data directory and navigate into it
mkdir data
cd data

# Create directories for Zookeeper
mkdir -p zookeeper/data/
mkdir -p zookeeper/log/

# Create directories for Kafka brokers
mkdir -p kafka/log/broker1/
mkdir -p kafka/log/broker2/
mkdir -p kafka/log/broker3/

# Create directories for checkpoints
mkdir -p checkpoint/filtered_news/
mkdir -p checkpoint/available_news/
mkdir -p checkpoint/processed_news/

# Create directory for Redis
mkdir redis/

# Create directory for PostgreSQL
mkdir postgres

# Create directory for MongoDB
mkdir mongodb/

# Create directory for Airflow logs
mkdir airflow-logs/

# Navigate back to the parent directory
cd ..
```

### Set Permissions

Set appropriate permissions for the created directories to ensure that the services can read from and write to these directories. Zookeeper and Kafka directories will have full permissions (777), while Redis, PostgreSQL, and MongoDB directories will have read, write, and execute permissions for the owner and read and execute permissions for others (755).

```bash
# Set permissions for Zookeeper directories
chmod -R 777 data/zookeeper/data/
chmod -R 777 data/zookeeper/log/

# Set permissions for Kafka broker directories
chmod -R 777 data/kafka/log/broker1/
chmod -R 777 data/kafka/log/broker2/
chmod -R 777 data/kafka/log/broker3/

# Set permissions for checkpoint directories
chmod -R 777 data/checkpoint/filtered_news/
chmod -R 777 data/checkpoint/available_news/
chmod -R 777 data/checkpoint/processed_news/

# Set permissions for Redis directory
chmod -R 755 data/redis/

# Set permissions for PostgreSQL directory
chmod -R 755 data/postgres/

# Set permissions for MongoDB directory
chmod -R 755 data/mongodb/

# Set permissions for Airflow logs directory
chmod -R 777 data/airflow-logs/
```

### Initialize Airflow

 Before starting the full Docker Compose setup, initialize Airflow. This step ensures that the necessary database migrations and initial setup are completed. Tipically, this creates an initial airflow user.

 ```bash
 docker compose up airflow-init -d
 ```

Acess airflow-init logs and assure that the intitialization was sucessful.
![alt text](resources/airflow-init-logs.png)


 ### Start All Services

```bash
docker compose up -d
```

### Acess Kafka and create topics

#### Acess kafka-brocker 1

```bash
docker exec -it kafka-broker1 bash
```

#### Create the topics

```bash
/scripts/create_topics.sh 
```
 
#### Describe the topics (Optional)

You can describe the topics by running the following command.

```bash
/scripts/describe_topics.sh
```

### Check topics creation

Go to Kafka UI to check the topics creation

Kafka UI is accessible via [localhost:7070](http://localhost:7070).

You should see  a login page

![alt text](resources/kafka-ui-login.png)

Fill your login informations, those you set in your kafka-ui/config.yml file.

After logging in, you should see something like the following image, after cliccking on **Topics**

![Kafka-UI-Topics](resources/kafka-ui-topics.png)

### Acess Spark master

You can acess Spark master via [localhost:9090](http://localhost:9090).

You should see the three Spark workers alive.
![Spark Master](resources/spark-master.png)


### Configure start hour and start days ago

You need to configure two variables in the config/config.py file.

- `START_HOUR`: This is the hour you need the news production start. I should be in [0-20]

In our case we set `START_HOUR` to 2 since we need our news production to starts at 2 AM. You may do the same for now.

- `START_DAYS_AGO`: The value of this variable depends on the day you want to DAGs start running, at the specified  `START_DAYS_AGO`, and should be less than or equal to 0. For exaple if you want it to run
  - the currrent day, set it to 1
  - tomorrow ie in one(1) day, set it to 0
  - in two(2) days, set it to -1 
  - in three(3) days, set it to -2
  - in four(4) days, set it to -3
  - in $n$ days, set it to $-(n-1)$


### Acess  airflow-webserver

Go to airflow-webserver. It is  is accessible via [localhost:8080](http://localhost:8080)

![airflow-login-page.png](resources/airflow-login-page.png)

On the logging page provide the logging informations you set in the airflow initialization command in the docker-compose.

#### Configure connection to Spark cluster

We need to create a connection to our Spark cluster in the Airflow admin. This allows Airflow to run some tasks using the Spark cluster.

On airflow webserver, go to Admin->connections

![Airflow admin connection](resources/airflow-admin-connection.png)

You should see this page

![Create connection](resources/create-connection.png)

Then click on the **Add a new record button**, ie the plus button. You will be redirected to the following page.

![Spark connection-1](resources/spark-connection-1.png)

You then need to fill the fields to get the connection created. 

As you can see, the **connection id** and the **connection type** are required

Set the connection id to spark-connection and the connection type to Spark

![Spark connection-2](resources/spark-connection-2.png)

![Spark connection-3](resources/spark-connection-3.png)


Two more fielda are available now and should be filled. There are the ***Host*** and the ***Port***.

Set the host to `spark://spark-master` and the port to `7077`, as done in the figure below. The description field is optional. 

Click on the save button 

![Spark connection-4](resources/spark-connection-4.png)


You should see something like

![Spark connection-5](resources/spark-connection-5.png)



### Access DAGs

Click on DAGs to access DAGs

![Click on DAGs](resources/click-dags.png)


 As you can see in the figure below there are four DAGs

 ![DAGs list](resources/dags-list.png)


### Activate the DAGs

Currently, the DAGs are paused. They wont never be executed until you active them

For each DAG, click on the ***Pause/Unpause DAG*** toggle to get it activated.

 ![Activate DAGs](resources/activate-dags.png)


Now everything is ready.

## Usage

### Trigger DAGs 

#### Trigger news producers DAG

![alt text](resources/news-production-dag.png)

Click on the news producer DAG and trigger it.

![alt text](resources/trigger-news-producer.png)


Make sure it runned successfully. You should see something like the image below.

![alt text](resources/news-producer-success.png)

Now go to Kafka UI and click on Topics. You will see that there are raw news messages produced to the RawNewsTopic, as can be seen on the figure below.

![alt text](resources/raw-news-topic.png)

Now acess RawNewsTopic->Messages

![alt text](resources/raw-news-topic-messages.png)

Then click on any message and you will see the message fields

![alt text](resources/raw-news-topic-message-fields.png)

#### Trigger news ETL DAG

![alt text](resources/news-etl-dag.png)

As done above with the news producer DAG, trigger the news ETL DAG.

Then make sure it runned successfully and here also acess Kafka UI->FilteredNewsTopic->Messages.

Then select any message.

You will see something like.

![alt text](resources/filtered-news-topic-message-field.png)


Acess Kafka UI->ProcessedNewsTopic->Messages.

Then select any message.

You will see something like.

![alt text](resources/processed-news-topic-message-field-1.png)

![alt text](resources/processed-news-topic-message-field-2.png)
![alt text](resources/processed-news-topic-message-field-3.png)

Run  the following command to acess MongoDB container shell

```bash
docker exec -it mongodb mongosh 
```

Swith to the news recommendation database

```bash
use use news_recommendation_db
```
Find and count MongoDB filtered news documents 

```bash
db.filtered_news.find()
```

```bash
db.filtered_news.countDocuments()
```

This is what our previous news message looks like in MongoDB

![alt text](resources/filtered-news-document.png)


The next DAG is the interactions storage DAG. But since there is no user interaction for now let us go to the news recommendation DAG but before, let us create a user

### Create a user

To create a user acess the newsengine-client container via via [localhost:8501](http://localhost:8501).

Fill the form and the OTP required.

Now that a user is created let us trigger the news recommendation DAG

### Trigger news recommendation DAG

Trigger the DAG, makesure it runned sucessfully and go to  Kafka UI->AvailableNewsTopic->Messages.

A message of that topic looks like 
![alt text](resources/available-news-topic-message-fields.png)


Now that the news are recommended this is what the user document looks like.

```bash
db.users.find()
```

![alt text](resources/user-document.png)


### Login to user account

Login to user account and see the recommended news, interact with the recommended news and go to Kafka UI->InteractionTopic->Messages

An ineraction message looks like


![alt text](resources/interactions-topic-message-fields.png)

Run streamlit app manually to be able to visialize the news on it's source

```bash
streamlit run app.py
```

### Trigger the interactions storage DAG

Trigger the interactions storage DAG to get the interactions stored and look at the user profile once again

```bash
db.users.find()
```

![alt text](resources/user-document.png)


Now that all DAGs have been triggered, go to your admin email address box and you should see the tasks execution emails.

![alt text](resources/email.png)


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

                
