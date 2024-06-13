from pyspark.sql.functions import col, lower, regexp_replace, trim, concat_ws
from pyspark.ml.feature import StopWordsRemover, Tokenizer
from nltk import download
from pyspark.ml import PipelineModel
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType, IntegerType

from pyspark.sql.types import DateType

# Download necessary NLTK data
download('wordnet')
download('vader_lexicon')
download('punkt')
download('stopwords')

class NewsPreprocessor:
    def __init__(self, lemmatize_udf): 
        # Initialize with user-defined lemmatization UDF
        self.lemmatize_udf = lemmatize_udf     
        # Load pre-trained LDA model for topic modeling
        self.lda_model = PipelineModel.load('../models/news_topic_model') 
        # Load pre-trained pipeline model for news categorization
        self.categorization_pipeline = PipelineModel.load('../models/news_categorization_model') 
        # Define schema for JSON data
        self.schema= StructType([
            StructField("title", StringType(), True),
            StructField("description", StringType(), True),
            StructField("content", StringType(), True),
            StructField("source_id", StringType(), True),
            StructField("source_name", StringType(), True),
            StructField("url", StringType(), True),
            StructField("img_url", StringType(), True),
            StructField("publication_date", IntegerType(), True),
            StructField("lang", StringType(), True),
            StructField("producer", StringType(), True),
        ])

    def clean(self, raw_articles):
        """
        Clean the raw articles by removing rows with missing URL, content, or description.
        Also clean and standardize the description text.
        """
        # Drop articles missing essential fields
        articles = raw_articles.na.drop(subset=['url', 'content', 'description'])
        
        # Clean and normalize the description
        articles = articles.withColumn(
            "description_cleaned",
            trim(
                regexp_replace(
                    regexp_replace(col("description"), r'[^a-zA-Z0-9\s]', ''),  # Remove special characters
                    r'\s+', ' '  # Replace multiple spaces with a single space
                )
            )
        )
        # Convert to lowercase
        articles = articles.withColumn("description_cleaned", lower(col("description_cleaned")))
        return articles

    def tokenize(self, cleaned_articles):
        """
        Tokenize the cleaned description text.
        """
        tokenizer = Tokenizer(inputCol="description_cleaned", outputCol="words")
        return tokenizer.transform(cleaned_articles)

    def lemmatize(self, tokenized_articles):
        """
        Apply the lemmatization UDF to the tokenized words.
        """
        df_lemmatized = tokenized_articles.withColumn("lemmas", self.lemmatize_udf(col("words")))
        return df_lemmatized
    
    def stopwords_removal(self, lemmatized_articles):
        """
        Remove stopwords from the lemmatized words.
        """
        remover = StopWordsRemover(inputCol="lemmas", outputCol="description_filtered")
        return remover.transform(lemmatized_articles)

    def transform(self, cleaned_articles, to_str=True):
        """
        Perform tokenization, lemmatization, and stopwords removal on the cleaned articles.
        Optionally convert the filtered words back to a single string.
        """
        tokenized_data = self.tokenize(cleaned_articles)
        lemmatized_data = self.lemmatize(tokenized_data)
        filtered_data = self.stopwords_removal(lemmatized_data)
        
        if to_str:
            # Convert filtered words list back to a single string
            filtered_data = filtered_data.withColumn("description_filtered_str", concat_ws(" ", "description_filtered"))
        
        return filtered_data

    def preprocess(self, articles, to_str=True):
        """
        Main preprocessing function to clean, transform, and preprocess the articles.
        """
        cleaned_data = self.clean(articles)
        transformed_data = self.transform(cleaned_data, to_str=to_str)
        return transformed_data