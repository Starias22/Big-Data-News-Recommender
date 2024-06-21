class FilteredNews:
    def __init__(self, id=None, title=None,
                  description=None, source_name=None,
                    url=None, img_url=None, publication_date=None, 
                    lang=None,author=None,category=None,sentiment=None):
        self.id = id
        self.title = title
        self.description = description
        
        self.source_name = source_name
        self.url = url
        self.img_url = img_url
        self.publication_date = publication_date
        self.lang = lang
        self.author=author
        self.category=category
        self.sentiment=sentiment
    def to_dict(self):
        return {
            "_id": self.id,
            "title": self.title,
            "description": self.description,
            "source_name": self.source_name,
            "url": self.url,
            "img_url": self.img_url,
            "publication_date": self.publication_date,
            "lang": self.lang,
            "author":self.author,
            "category":self.category,
            "sentiment_score":self.sentiment
        }
    
    def to_dict_persist(self):
        return {
            "_id": self.id,
            "title": self.title,
            "description": self.description,
            "source_name": self.source_name,
            "url": self.url,
            "img_url": self.img_url,
            "publication_date": self.publication_date,
            "lang": self.lang,
            "author":self.author,
        }

    @staticmethod
    def from_dict(data):
        return FilteredNews(
            id=data.get('_id'),
            title=data.get('title'),
            description=data.get('description'),
            source_name=data.get('source_name'),
            url=data.get('url'),
            img_url=data.get('img_url'),
            publication_date=data.get('publication_date'),
            lang=data.get('lang'),
            author=data.get('author'),
            category=data.get('category'),
            sentiment=data.get('sentiment_score')
        )
    
    @staticmethod
    def from_dict_persist(data):
        return FilteredNews(
            id=data.get('_id'),
            title=data.get('title'),
            description=data.get('description'),
            source_name=data.get('source_name'),
            url=data.get('url'),
            img_url=data.get('img_url'),
            publication_date=data.get('publication_date'),
            lang=data.get('lang'),
            author=data.get('author')
        )

    def display(self):
        print('News ID:', self.news_id)
        print('Title:', self.title)
        print('Description:', self.description)
        print('Source Name:', self.source_name)
        print('URL:', self.url)
        print('Image URL:', self.img_url)
        print('Publication Date:', self.publication_date)
        print('Language:', self.lang)
