# moving all forms that are for a user and autherntication
# as we are making a blueprint 
from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user 
from flaskblog.models import User



# python class to represent a registration form 
# inherits from flask form and fields are imported classes from wtforms 
# username is the label in html 
# use a validator to make some limitations e.g. max characters
# these are arguments to pass into a field

# This class handles a users registration

class RegistrationForm(FlaskForm): 
    username = StringField('Username', validators = [DataRequired(), 
                                                     Length(min =2,max = 30)])
    email = StringField('Email', 
                        validators= [DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    # custom validation: 
    # we are checking if the username is already in the database
    def validate_username(self, username): 

        # checks if username is in the database
        # username.data is coming from the form
        user = User.query.filter_by(username = username.data).first()

        if user: 
            raise ValidationError('That username is taken, choose a different one!')
        
    # check that the email is unique too: 
    def validate_email(self, email): 

        # grabs email data: 
        user = User.query.filter_by(email = email.data).first() 

        if user: 
            raise ValidationError('That email has been taken')

    
# This class handles a users Login Form: 

class LoginForm(FlaskForm): 

    email = StringField('Email', 
                        validators= [DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
    

# This class handles updating the user account information

class UpdateAccountForm(FlaskForm): 
    # files to update account information 
    username = StringField('Username', validators = [DataRequired(), 
                                                     Length(min =2,max = 30)])
    email = StringField('Email', 
                        validators= [DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')

    # custom validation: 
    # we are checking if the username is already in the database
    def validate_username(self, username): 

        # checks that the username is differnt from curretn username 
        # because the session is the current_user
        # only run checks if its different

        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user: 
                raise ValidationError('That username is taken, choose a different one!')
        
    # check that the email is unique too: 
    def validate_email(self, email): 

        # grabs email data: 
        # if the email address is differnt to the current users then allow a change 
        # validation check is for this: 
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first() 

            if user: 
                raise ValidationError('That email has been taken')
            


# create some new forms to rset a email and a password
# form to reset the password page 
# submit their email for their account
# where the instructions for reseting password will be sent 

class RequestResetForm(FlaskForm): 

    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    # we have to check that a email exists 
    # otherwise they have to create an email address
    submit = SubmitField('Request Password Reset')

    # check if the email does not exist: 
    # check if an account exists for this email 
    # which means they did not create an account - like on resgistaration
        # check that the email is unique too: 
        # we want to check if the email does not exists
    def validate_email(self, email): 

        # grabs email data: 
        user = User.query.filter_by(email = email.data).first() 

        if user is None: 
            raise ValidationError('There is no account associated with this Email. You must register First!')
        
# class to rest the password: 
class ResetPasswordForm(FlaskForm): 
    # two fields to confirm passwords and submit: 
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), 
                                                 EqualTo('password')])
    
    submit = SubmitField('Reset Password')
    # create routes and templates that handles forms
