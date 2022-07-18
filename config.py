import os

# Use class to store all config variables 
# And could access it with python property fields
class Config():
    # checks for security reasons
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\xe3\x0eRTP;4\xc7\xc0k&\xa9\xf0k<H'

    MONGODB_SETTINGS =  { 'db' : 'UTA_Enrollment' }
    
