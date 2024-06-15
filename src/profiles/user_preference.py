class UserPreference:
    def __init__(self, user_id, categories=[], sentiments=[], seen_news=[]):
        self.user_id = user_id
        self.categories = categories
        self.sentiments = sentiments 
        self.seen_news = seen_news 
        

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "categories": self.categories,
            "sentiments": self.sentiments,
            "seen_news": self.seen_news,
        }

    @staticmethod
    def from_dict(data):
        return UserPreference(
            user_id=data['user_id'],
            categories=data.get('categories', []),
            sentiments=data.get('sentiments', []),
            seen_news=data.get('seen_news', []),
            
        )
