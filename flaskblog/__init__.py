# make a package with the name of our applicaiton 
# init file makes this a package in top level
# folder has same name as our applcation so flaskblog/ = flaskblog app 
# initialise the application

# import flask class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail # helps us send emails
# to use the config files we just set 
# use app.config from object method 
from flaskblog.config import Config 
# app is an instance of flask viarable 
# __name__ is the name of the module, this is the same as main - so flask knows where to look
# app = Flask(__name__)

# url-for finds the routes finds the location of teh routes for us.
#
# 

# below usese the class from the config 
# these are the config values we have set
# can set other config settings like a debug mode
# app.config.from_object(Config) 

# set a secret key to stop people messing with the app
# app.config['SECRET_KEY'] = 'fea587cc66094ff6e53b8b3288d38d0d'
# # set a location for the sql database: 
# # relative path from the current file
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

# create database instance
db = SQLAlchemy() 
# db = SQLAlchemy(app)
# you create the instance of the database 
# load into python and from flaskblog import db 
# then import models, flaskblog.models import User, Post, 
# from flaskblog import app
# app.app_context().push()
# db.create_all()
# test with User.query.all()

# adding in encryption hasing for user password 
# bcrypt = Bcrypt(app)

bcrypt = Bcrypt()

# Adding a login manager so that we can handle user logins 
# login_manager = LoginManager(app)

login_manager = LoginManager()

# where the login will work: 
# samne as url_for 
# login manager now users blueprint
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# making confirm variables for the mail: 
# thi si show the app knows how to send emails 
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# use the environment variables for email account:
# these are going to be set to my username and password
#  we set them in environment variables for sercurity purposes
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# # password for email: 
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# apps configs have been moved

# we can no wintiailize exteision


# mail = Mail(app)

mail = Mail()

# import the routes - improt the bluepirnt objects
# from flaskblog.users.routes import users # this is the blueprint instance
# from flaskblog.posts.routes import posts 
# from flaskblog.main.routes import main 
# # register the blueprint
# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)
# from flaskblog import routes

# create a function so that 
# we can make an app - allows us to make different instances
# with different configutations like prod and test 
# takes in which config object we want to use for our app

# creation of application is made here
# extensions that we use remain outside of the function
# as app has now changed, we amend the extensions
# we dont move extensions as we want them created outside of the function 
# but we do want to initialize these inside of the function with the application 
# from flask docs - this is so extension object does not get bound to the object 
# so initialize etensions wihtout app at top of file 
# then use init app method to pass the application to all the extensions:

def create_app(config_class = Config): 
    app = Flask(__name__)
    app.config.from_object(Config) 

    # run the init app method: 
    db.init_app(app)
    bcrypt.init_app(app) 
    login_manager.init_app(app)
    mail.init_app(app)
    # this is the blueprint instance
    from flaskblog.users.routes import users 
    from flaskblog.posts.routes import posts 
    from flaskblog.main.routes import main
    # import the blueprint to handle errors
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    # register the errors blueprin t
    app.register_blueprint(errors)

    return app 

# the app variable no longer exists in teh flaskblog package 
# so we replace app variabl ewith flask import called current app 