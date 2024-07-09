from nltk import download, data
from config.config import NLTK_DATA_PATH


data.path = [NLTK_DATA_PATH]

print("NLTK data path:", data.path)

# NDownload useful NLTK resources
download('wordnet', download_dir=NLTK_DATA_PATH) # For lemmatization
download('vader_lexicon',download_dir=NLTK_DATA_PATH) # For sentiment analysis


