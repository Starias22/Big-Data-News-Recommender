
# News Data Preprocessing for News Categorization

## Introduction

This section details the preprocessing steps applied to the news data to prepare it for categorization in our news recommendation system. The process involves data loading, cleaning, transformation, integration, augmentation, and balancing to ensure the dataset is suitable for training machine learning models.

## I. Data Source

The datasets are sourced from multiple CSV files and a JSON file containing news articles. These datasets include various fields such as title, description, category, and publication date. The data include four CSV files and one JSON file, collected from old news archives shared via Kaggle.

### Dataset Links

1. [Topic-labeled news dataset](https://www.kaggle.com/datasets/kotartemiy/topic-labeled-news-dataset)
2. [News categories dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset)
3. [Environment news dataset](https://www.kaggle.com/datasets/beridzeg45/guardian-environment-related-news)
4. [Business and Financial news dataset](https://www.kaggle.com/datasets/thedevastator/cnbc-business-and-financial-news-dataset-450k)
5. [Indian financial news articles dataset](https://www.kaggle.com/datasets/hkapoor/indian-financial-news-articles-20032020)

## II. Preprocessing Each Dataset

Each of the five datasets collected has been preprocessed. The following operations have been performed on them.

### Loading the Dataset

The preprocessing begins by loading the news datasets into a Spark DataFrame. Spark is used to handle large datasets efficiently. The data is read from CSV or JSON files, ensuring the header information is included.

### Dealing with Null Values

The dataset is checked for null values in the 'description' column, which is crucial for news categorization. Any records with null descriptions are replaced by the title column if it exists and is not null. Otherwise, these records are removed to ensure data quality.

### Feature Selection

Finally, only the relevant columns such as filtered description and news category have been selected.


## III. Data Integration

### Merging Datasets

The data integration begins with joining the five dataframes obtained in the previous step. The news datasets from different sources are merged into a single cohesive dataset. The merged dataset provides a comprehensive view of the news articles from various sources.

### Resolving Duplicates

After merging, the dataset is checked for duplicate records. Duplicate entries are removed to ensure that each news article is unique and to avoid bias in the data analysis and modeling steps.

### Reducing the Categories

The dataset was grouped by descending order of instances of each class, resulting in 48 classes initially. These were further grouped to reduce the number of classes to 16:

- Group `"ARTS"`, `"CULTURE & ARTS"`, `"ARTS & CULTURE"`, `"SPORTS"`, `"COMEDY"`, and `"ENTERTAINMENT"` to `"ENTERTAINMENT-ARTS-CULTURE"`
- Group `"MONEY"`, `"BUSINESS"`, `"BUSINESS & FINANCE"` to `"BUSINESS-ECONOMY-FINANCE"`
- Group `"NATION"`, `"U.S. NEWS"`, `"WORLD NEWS"`, `"THE WORLDPOST"`, `"WORLDPOST"`, `"WORLD"` to `"NATION & WORLD"`
- Group `"SCIENCE"`, `"TECH"`, `"TECHNOLOGY"` to `"SCIENCE & TECHNOLOGY"`
- Group `"COLLEGE"`, `"EDUCATION"` to `"EDUCATION"`
- Group `"HEALTHY LIVING"`, `"HEALTH"` to `"HEALTH & WELLNESS"`
- Group `"PARENTS"`, `"PARENTING"`, `"WEDDINGS"`, `"DIVORCE"` to `"FAMILY & RELATIONSHIP"`
- Group `"GREEN"`, `"ENVIRONMENT"` to `"ENVIRONMENT"`
- Group `"STYLE"`, `"STYLE & BEAUTY"`, `"HOME & LIVING"` to `"LIFESTYLE"`
- Group `"TASTE"`, `"FOOD & DRINK"`, `"TRAVEL"` to `"TRAVEL & FOOD"`
- Group `"BLACK VOICES"`, `"QUEER VOICES"`, `"WOMEN"`, `"LATINO VOICES"` to `"SOCIAL ISSUES"`
- Group `"WEIRD NEWS"`, `"GOOD NEWS"`, `"FIFTY"` to `"MISCELLANEOUS"`

After that, we removed classes that may lead to confusion, such as `"MISCELLANEOUS"`, `"SOCIAL ISSUES"`, `"NATION & WORLD"`, `"IMPACT"`, and finally, we got 12 categories of news:

1. BUSINESS-ECONOMY-FINANCE
2. ENTERTAINMENT-ARTS-CULTURE
3. ENVIRONMENT
4. HEALTH & WELLNESS
5. POLITICS
6. SCIENCE-TECHNOLOGY-MEDIA
7. FAMILY & RELATIONSHIP
8. TRAVEL & FOOD
9. LIFESTYLE
10. CRIME
11. RELIGION
12. EDUCATION

### Removing Empty Descriptions

Any records with empty descriptions are removed from the dataset to ensure that all remaining records have meaningful content for analysis and modeling. This involves:

- Removing the rows with empty descriptions.
- Removing rows with probably non-meaningful descriptions, such as rows with less than 15 letters or three words.

### Feature Encoding

Machine learning algorithms need numerical data, so we converted our category column to numerical values in the range [0, 12]. The mapping of numerical values to their categories has been saved to a JSON file.

### Data Augmentation

To enhance the dataset and improve model performance, data augmentation techniques are applied using NLPAug. This involves generating synthetic data by slightly modifying the existing news descriptions while preserving their original meaning. Augmentation helps in increasing the diversity and size of the training dataset, making the models more robust.

NLPAug supports the following methods of data augmentation:

- Synonym Replacement: Randomly choose n words from the sentence that are not stop words. Replace each of these words with one of its synonyms chosen at random.
- Random Swap: Randomly choose two adjacent words in the sentence and swap their positions.
- Random Deletion: Randomly remove each word in the sentence.
- Antonym Replacement: Randomly choose n words from the sentence that are not stop words. Replace each of these words with one of its antonyms chosen at random.

The method used is Synonym Replacement. As a word source to augment our data, we used WordNet.

### Text Cleaning: Removing Special Characters

Special characters, punctuation, and extra spaces are removed from the descriptions to clean the text and maintain only alphanumeric characters. This step is essential for simplifying the text data and improving the performance of tokenization and other text processing techniques.

### Text Transformation

#### Lowercasing

To maintain consistency, all text in the 'description' column is converted to lowercase. This step helps in reducing the complexity of text data by treating words with different cases as identical.

#### Tokenization

The cleaned text descriptions are split into individual words or tokens. Tokenization helps in breaking down the text into manageable pieces for further processing.

#### Lemmatization

Lemmatization is applied to convert words to their base or root form. This step helps in normalizing the text data by reducing different forms of a word to a single form, making it easier to analyze.

#### Stop Words Removal

Common stop words (e.g., 'and', 'the', 'is') that do not contribute significant meaning to the text are removed. This step helps in reducing noise in the data and focusing on the more meaningful words.

### Handling Empty Descriptions

After removing stop words, the dataset is checked for any empty or duplicate descriptions that may result from these transformations. The concerned rows are removed.

### Data Balancing

The number of records in each news category is counted to identify, once again, any imbalances in the dataset. Although we have already applied data augmentation to balance our data, there may still be imbalances due to the previous removed rows.

To address imbalances, the dataset is balanced by undersampling majority classes. This step ensures that the machine learning models trained on the data do not become biased towards any particular category.

This final version of our balanced news dataset contains

- 65028 rows
- 12 categories of news
- 2 columns which are filtered description and numerical category


## Saving the Preprocessed Data

The final balanced dataset is saved in both CSV and Parquet formats. These formats are chosen for their efficiency and compatibility with various data processing tools.

## Conclusion

The preprocessing steps described above ensure that the news dataset is clean, consistent, and balanced, making it suitable for training robust news categorization models. These steps form a crucial part of the data preparation phase in the development of a news recommendation system.
