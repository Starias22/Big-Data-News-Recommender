class UserPreference:
    def __init__(self, user_id, categories=None, sentiments=None, seen_news=None, liked_news=None, disliked_news=None):
        self.user_id = user_id
        self.categories = categories if categories else []
        self.sentiments = sentiments if sentiments else []
        self.seen_news = seen_news if seen_news else []
        

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
