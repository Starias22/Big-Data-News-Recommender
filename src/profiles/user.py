class User:
    def __init__(self, id=None, firstname=None, lastname=None, email=None,
                 categories=[i for i in range(32)], sentiments=[0,-1,1], seen_news=[],
                 ansa=True):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.categories = categories
        self.sentiments = sentiments
        self.seen_news = seen_news 
        self.ansa=ansa

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "categories": self.categories,
            "sentiments": self.sentiments,
            "seen_news": self.seen_news,
            "ansa":self.ansa
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data.get('_id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa')
        )

    @staticmethod
    def retrieve_preferences(data):
        return User(
            id=data.get('_id'),
            categories=data.get('categories'),
            sentiments=data.get('sentiments'),
            seen_news=data.get('seen_news'),
            ansa=data.get('ansa'),
            email=data.get('email'),

        )

    def display(self):
        print('Firstname:', self.firstname)
        print('Lastname:', self.lastname)
        print('Email:', self.email)
