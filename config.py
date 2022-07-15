import os

# Use class to store all config variables 
# And could access it with python property fields
class Config():
    # checks for security reasons
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    MONGODB_SETTINGS =  { 'db' : 'UTA_Enrollment' }
    
