# creating forms and validate user inputs 
# using flask-wtf package to create forms
# python classes represent the forms, and html converts in the termplate
from flask_wtf import FlaskForm

# import file upload 
from flask_wtf.file import FileField, FileAllowed
# these are fiels that we import from the wt froms package
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
#t hese are validators they help set some conditions on the form inputs
# some are lenghts and valid emails others are just values equal to
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

# flask login import current user this will handle updating user account information
from flask_login import current_user


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
            
# A new class form to create a  psot : 
class PostForm(FlaskForm): 
    # validator as every title needs to exist
    title = StringField('Title', validators=[DataRequired()])
    # text area field is needed for the post 
    # every post needs content
    content = TextAreaField('Content', validators=[DataRequired()])
    # submit the field: 
    submit = SubmitField('Post')