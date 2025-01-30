import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



# dummy data: 
# can be used int he template for home.html using jinja 
posts = [

    {'title': 'Bond Market',
     'author': 'john Doe', 
     'content': 'HSBC' , 
     'date_posted': '01-01-2024'
     }, 

    {'title': 'Gilts Market',
     'author': 'John Smith', 
     'content': 'JP Morgan', 
     'date_posted': '01-01-2024'
     } 


]




# routesare where to go to different pages 
# made using route decorators
# this function returns the info on this site, here it is text 
# envronment variable is set to run the flask app using $env
# have server running in debug mode
# two routes can be handled by the same function
@app.route("/")
@app.route("/home")
# render the template from the templates directory
def home(): 
    return render_template('home.html', posts = posts)

# about page route: 
@app.route("/about")
def about(): 
    return render_template('about.html', title = "About Page")

# creating routes for registrationa nd logn 
# placing in get and post methods 
# check for post data valid for the form
# we will add in password hashing 
# and also add a custom validation for the form when signing up to avoid dupliacte users
@app.route("/register", methods = ['GET', 'POST'])
def register(): 

    # if the user is already loggined in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('home'))


    form = RegistrationForm()
    if form.validate_on_submit(): 
        # setting password 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create a new user 
        user = User(username = form.username.data, 
                    email = form.email.data, 
                    password = hashed_password)
        
        # add user to database 
        db.session.add(user)
        # commit change to database 
        db.session.commit()
        flash('Your account has been created! You can now Login', 'success')
        return redirect(url_for('login'))
    
    # else if there is no user form submitted its just the register page
    return render_template('register.html', title = "Register", form =form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if the user is already logged in: 
    if current_user.is_authenticated: 
        # go to the home page: 
        return redirect(url_for('home'))



    form = LoginForm()
    if form.validate_on_submit():
        # checks that the email entered into the form matches our database
        # checking the database if username is valid and password: 
        user = User.query.filter_by(email = form.email.data).first()
        # checks that password is correct too: 
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            # if user exists and password is valid then log the user in: 
            login_user(user, remember = form.remember.data)
            # to return a user to the correct website they were viewing before logging in 
            next_page = request.args.get('next')


            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


# create logout route: 
# redirects to home
@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for('home'))

# save picture: 
def save_picture(form_picture): 
    # saves the users picture, but not the filename: 




# adding a route for account 
# when a user is loggined in they will see this route: 
# login required decoretor so you can access when logged in 
# you have to tell the extension where the login route is located
@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account(): 
    # create instance of the updating account information form: 
    form = UpdateAccountForm()

    if form.validate_on_submit(): 
            # if the form uis valid we can update our curren tusername and email and photo
            # can change values from current user varaibles
            # changing current user values for username and email from the form 

        # checl that a picture exists: 
        
        current_user.username = form.username.data
        current_user.email = form.email.data 
        # commit to the database
        db.session.commit()
        # add user image: 
        flash('Your Account has been Updated!', 'success')
        # This avoids reloading POST requests constantly 
        return redirect(url_for('account'))
    # else conditional to check if its a get request 
    # so we can populate the fields with current user information
    elif request.method == 'GET': 
        form.username.data = current_user.username 
        form.email.data = current_user.email




    # setting the image file to be sent to acccount template
    # this will take teh image_file used when making the account
    # we have default image that is used
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)