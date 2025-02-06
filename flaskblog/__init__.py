# make a package with the name of our applicaiton 
# init file makes this a package in top level
# folder has same name as our applcation so flaskblog/ = flaskblog app 
# initialise the application

# import flask class
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail # helps us send emails
# app is an instance of flask viarable 
# __name__ is the name of the module, this is the same as main - so flask knows where to look
app = Flask(__name__)
# url-for finds the routes finds the location of teh routes for us. 

# set a secret key to stop people messing with the app
app.config['SECRET_KEY'] = 'fea587cc66094ff6e53b8b3288d38d0d'
# set a location for the sql database: 
# relative path from the current file
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"

# create database instance 
db = SQLAlchemy(app)
# you create the instance of the database 
# load into python and from flaskblog import db 
# then import models, flaskblog.models import User, Post, 
# from flaskblog import app
# app.app_context().push()
# db.create_all()
# test with User.query.all()

# adding in encryption hasing for user password 
bcrypt = Bcrypt(app)

# Adding a login manager so that we can handle user logins 
login_manager = LoginManager(app)

# where the login will work: 
# samne as url_for 
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# making confirm variables for the mail: 
# thi si show the app knows how to send emails 
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# use the environment variables for email account:
# these are going to be set to my username and password
#  we set them in environment variables for sercurity purposes
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# password for email: 
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# we can no wintiailize exteision
mail = Mail(app)

# import the routes 
from flaskblog import routes