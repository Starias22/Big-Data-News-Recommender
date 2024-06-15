class User:
    def __init__(self, id=None,firstname=None, lastname=None, email=None,
                 categories=[],
                 sentiments=[],seen_news=[]):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.categories=[]
        self.sentiments=[]
        self.seen_news=[]


    def to_dict(self):
        return {
            #"id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            #"preferences":
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data.get('_id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email']
        )

    def display(self):
        print('Firstname:',self.firstname)
        print('Lastname:',self.lastname)
        print('Email:',self.email)