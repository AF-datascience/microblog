# Place all config values here 
# makes application easier to test 
# moves config of app into a function so we can make diff configurations
# making class based, so all configs are stored in am object

# this is the class config 
# best practise is to move out some of these vaues into the source code
# we can use this for the secreate key and database uri 
# but if we use like postgres or online db, these will be in connection string
# so set these in environment vairables just like email user and email pass
import os 


class Config: 

    # set a secret key to stop people messing with the app
    # 'SECRET_KEY' = 'fea587cc66094ff6e53b8b3288d38d0d'
    # set a location for the sql database: 
    # relative path from the current file
    # 'SQLALCHEMY_DATABASE_URI' = "sqlite:///site.db"

    # get secret key and database uri using os variable 
    # these are the environment variables that we set earlier: 
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # these are all ocnfigurations 
    # making confirm variables for the mail: 
    # thi si show the app knows how to send emails 
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # use the environment variables for email account:
    # these are going to be set to my username and password
    #  we set them in environment variables for sercurity purposes
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # password for email: 
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')