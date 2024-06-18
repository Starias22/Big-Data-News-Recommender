class FilteredNews:
    def __init__(self, news_id=None, title=None, description=None, source_id=None, source_name=None, url=None, img_url=None, publication_date=None, lang=None):
        self.news_id = news_id
        self.title = title
        self.description = description
        self.source_id = source_id
        self.source_name = source_name
        self.url = url
        self.img_url = img_url
        self.publication_date = publication_date
        self.lang = lang

    def to_dict(self):
        return {
            "news_id": self.news_id,
            "title": self.title,
            "description": self.description,
            "source_id": self.source_id,
            "source_name": self.source_name,
            "url": self.url,
            "img_url": self.img_url,
            "publication_date": self.publication_date,
            "lang": self.lang
        }

    @staticmethod
    def from_dict(data):
        return FilteredNews(
            news_id=data.get('news_id'),
            title=data.get('title'),
            description=data.get('description'),
            source_id=data.get('source_id'),
            source_name=data.get('source_name'),
            url=data.get('url'),
            img_url=data.get('img_url'),
            publication_date=data.get('publication_date'),
            lang=data.get('lang')
        )

    def display(self):
        print('News ID:', self.news_id)
        print('Title:', self.title)
        print('Description:', self.description)
        print('Source ID:', self.source_id)
        print('Source Name:', self.source_name)
        print('URL:', self.url)
        print('Image URL:', self.img_url)
        print('Publication Date:', self.publication_date)
        print('Language:', self.lang)


"""
# Example usage
# Create a FilteredNews instance
news_instance = FilteredNews(
    news_id="12345",
    title="Sample News Title",
    description="This is a sample news description.",
    source_id="source_001",
    source_name="Sample Source",
    url="http://example.com/sample-news",
    img_url="http://example.com/sample-image.jpg",
    publication_date="2024-06-16",
    lang="en"
)

# Display information
news_instance.display()

# Convert to dictionary
news_dict = news_instance.to_dict()
print(news_dict)

# Create a FilteredNews instance from dictionary
new_news_instance = FilteredNews.from_dict(news_dict)
new_news_instance.display()
"""