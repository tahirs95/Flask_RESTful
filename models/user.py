import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users where username=?"
        # result = cursor.execute(query, (username,)) #username should always be tuple.
        # row = result.fetchone()
        # if row:
        #     # user = User(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        
        # connection.close()
        # return user
        # return cls.query # SELECT * from users
        return cls.query.filter_by(username=username).first()
            
    @classmethod
    def find_by_id(cls, _id):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM users where id=?"
        # result = cursor.execute(query, (_id,)) #username should always be tuple.
        # row = result.fetchone()
        # if row:
        #     # user = User(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        
        # connection.close()
        # return user
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()