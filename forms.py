# creating forms and validate user inputs 
# using flask-wtf package to create forms
# python classes represent the forms, and html converts in the termplate
from flask_wtf import FlaskForm
# these are fiels that we import from the wt froms package
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#t hese are validators they help set some conditions on the form inputs
# some are lenghts and valid emails others are just values equal to
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
    
# Thsi class handles a users Login Form: 

class LoginForm(FlaskForm): 

    email = StringField('Email', 
                        validators= [DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
    