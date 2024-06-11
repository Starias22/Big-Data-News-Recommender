from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, ArrayType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml.clustering import LDA
from nltk.corpus import stopwords
from nltk import download, WordNetLemmatizer
import json
import re

# Download necessary NLTK data
download('stopwords')
download('wordnet')

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("LDAPipelineExample") \
    .getOrCreate()

# Example dataset
data = [
    {"text": "The economy is improving according to recent reports."},
    {"text": "New technologies are emerging in the field of artificial intelligence."},
    {"text": "Climate change is a significant concern for the future."},
    {"text": "Healthcare advancements are being made every day."},
    {"text": "Education systems need to adapt to new learning methods."},
    {"text": "The economy is improving according to recent reports."},
    {"text": "New technologies are emerging in the field of artificial intelligence."},
    {"text": "Climate change is a significant concern for the future."},
    {"text": "Healthcare advancements are being made every day."},
    {"text": "Education systems need to adapt to new learning methods."}

]

# Create DataFrame from example data
df = spark.createDataFrame(data)

# Define preprocessing functions
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if text:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.strip()
    return ''

clean_text_udf = udf(clean_text, StringType())

def lemmatize_tokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

lemmatize_udf = udf(lemmatize_tokens, ArrayType(StringType()))

# Apply text cleaning
df = df.withColumn("cleaned_text", clean_text_udf(col("text")))

# Define the stages of the pipeline
tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="tokens")
remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")


vectorizer = CountVectorizer(inputCol="filtered_tokens", outputCol="raw_features", vocabSize=100)
idf = IDF(inputCol="raw_features", outputCol="features")
lda = LDA(k=3, maxIter=10, featuresCol="features")  # Small number of topics for simplicity

# Create the pipeline
pipeline = Pipeline(stages=[tokenizer, remover, vectorizer, idf, lda])

# Split the data into train and test sets
train_df, test_df = df.randomSplit([0.8, 0.2], seed=1234)

# Fit the pipeline on the training data
pipeline_model = pipeline.fit(train_df)

pipeline_model.save("/tmp/pipeline_model")
# Save the fitted pipeline
#pipeline_model.write().overwrite().save("/tmp/pipeline_model")

# Load the saved pipeline model
from pyspark.ml import PipelineModel
pipeline_model = PipelineModel.load("/tmp/pipeline_model")

# Transform the test data
test_topics = pipeline_model.transform(test_df)

# Show the topics distribution
test_topics.select("topicDistribution").show(truncate=False)

spark.stop()
