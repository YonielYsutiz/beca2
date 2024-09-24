from db_config import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    number_phone = db.Column(db.String)
    fullname = db.Column(db.String)
    age = db.Column(db.Integer)

    def __resp__(self):
        return "<User %r>" % self.username
    
# def __init__(self, id, username, password, number_phone, email, fullname="",   ) -> None:
#     self.id = id
#     self.username = username
#     self.password = password
#     self.fullname = fullname
#     self.number_phone = number_phone
#     self.email = email

# @classmethod
# def check_password_hash(self, hashed_password, password):
#     return check_password_hash(hashed_password, password) 