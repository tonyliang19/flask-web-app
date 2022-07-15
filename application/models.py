import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

# This file should containts all models beloging to collections of the database

# Use a class to represent a user and maps this to db
class User(db.Document):
    # Assert every user id is unique
    user_id     = db.IntField(unique=True)
    # You could change the length to other
    first_name  = db.StringField(max_length=50)
    last_name   = db.StringField(max_length=50)
    email       = db.StringField(max_length=30, unique=True)
    # Length of password would then set to 128 or more, since hash is long        
    password    = db.StringField( )
    # This generates unique hash value for password of the use
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # This gets the password and checks it 
    def get_password(self, password):
        return check_password_hash(self.password, password)

    
    


class Course(db.Document):
    # Assert every user id is unique
    course_id   = db.StringField(max_length = 10, unique=True)
    # You could change the length to other
    title       = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits     = db.IntField()
    term        = db.StringField(max_length=25)


# Junction table, many-to-many relationships
# that can combine information of two or more tables
class Enrollment(db.Document):
    user_id = db.IntField()
    course_id = db.StringField(max_length=10)
    
