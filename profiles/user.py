class User:
    def __init__(self, id,firstname, lastname, email):
        self.id=id
        self.firstname=firstname
        self.lastname=lastname
        self.email=email


    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data):
        return User(
            user_id=data.get('id'),
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email']
        )
