from datetime import datetime

class Interaction:
    def __init__(self, id=None, user_id=None, features=None,
                 topicDistribution=None, category=None, sentiment=None,news_id=None,
                 action=None,date=int(datetime.now().timestamp())):
        self.id = id
        self.user_id = user_id
        self.news_id=news_id
        self.features = features
        self.topicDistribution = topicDistribution
        self.category = category
        self.sentiment = sentiment
        self.action=action
        self.date=date

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "features": self.features,
            "news_id": self.news_id,
            "action": self.action,
            "date": self.date  # Convert datetime to ISO format string
        }
    
    def to_dict_persist(self):
        return {
            "news_id": self.news_id,
            "features": self.features,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Interaction(
            id=data.get('_id'),
            user_id=data.get('user_id'),
            features=data.get('features'),
            topicDistribution=data.get('topicDistribution'),
            category=data.get('category'),
            sentiment=data.get('sentiment'),
            news_id=data.get('news_id'),
            action=data.get('action'),
            date=data.get('date')

        )

    @staticmethod
    def retrieve_preferences(data):
        return Interaction(
            id=data.get('id'),
            user_id=data.get('user_id'),
            features=data.get('features'),
            topicDistribution=data.get('topicDistribution'),
            category=data.get('category'),
            sentiment=data.get('sentiment'),
            news_id=data.get('news_id')

        )

    def display(self):
        print('ID:', self.id)
        print('User ID:', self.user_id)
        print('Features:', self.features)
        print('Topic Distribution:', self.topicDistribution)
        print('Category:', self.category)
        print('Sentiment:', self.sentiment)
        print('News ID:', self.news_id)
        print('Action:', self.action)
        print('date:', self.date)



# Example usage
# Create an Interaction instance
interaction_instance = Interaction(id='userid', user_id=100, features=[],
                                    topicDistribution=[], category=1, 
                                    sentiment=0)

# Display information
interaction_instance.display()

# Convert to dictionary
interaction_dict = interaction_instance.to_dict()
print(interaction_dict)

# Create an Interaction instance from dictionary
new_interaction_instance = Interaction.from_dict(interaction_dict)
new_interaction_instance.display()
